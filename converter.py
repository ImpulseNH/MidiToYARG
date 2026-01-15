import shutil
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any, Tuple
from mido import MidiFile, MidiTrack, MetaMessage, Message

from mappings import DRUM_MAPPING, IS_TOM, TOM_MARKERS_MAP

# Config
NOTE_LEN = 1
MIN_VELOCITY = 40

class MidiToYARGConverter:
    """
    Handles the conversion of raw MIDI files into YARG/Clone Hero compatible charts.
    Includes logic for tempo mapping, beat generation, and strict limb-limit humanization.
    """

    def process_song(self, midi_path: str, metadata: Dict[str, Any], output_dir: str) -> str:
        """
        Main pipeline entry point. Prepares directories and orchestrates track generation.
        """
        out_path = Path(output_dir)
        
        # Clean folder name
        artist = self._clean_name(metadata.get("artist", "Unknown"))
        song = self._clean_name(metadata.get("name", "Untitled"))
        folder = out_path / f"{artist} - {song}"

        # Wipe previous output to avoid stale files during iterative testing
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True, exist_ok=True)

        # Core generation
        self._create_chart(midi_path, str(folder / "notes.mid"))
        self._create_ini(metadata, folder)

        return str(folder)

    def _clean_name(self, text: str) -> str:
        return "".join(c for c in text if c.isalnum() or c in " -_.").strip()

    def _create_chart(self, input_path: str, output_path: str) -> None:
        """
        Rebuilds the MIDI structure. Uses Type 1 to allow separate Tempo and Instrument tracks.
        """
        mid_in = MidiFile(input_path)
        # Type 1 is required for multi-track (Tempo Map + Notes)
        mid_out = MidiFile(type=1, ticks_per_beat=mid_in.ticks_per_beat)

        # 1. Build Tempo Map (Track 0)
        tempo_track = MidiTrack()
        tempo_track.name = "Tempo Map"
        mid_out.tracks.append(tempo_track)

        tempo_events = []
        abs_time = 0
        
        # Flatten track 0 events to absolute time for easier processing
        for msg in mid_in.tracks[0]:
            abs_time += msg.time
            if msg.type in ("set_tempo", "time_signature"):
                tempo_events.append((abs_time, msg))

        # Write tempo events with delta times
        last_t = 0
        for t, msg in tempo_events:
            tempo_track.append(msg.copy(time=t - last_t))
            last_t = t

        # Calculate total song duration in ticks for the Beat Track
        total_ticks = max((sum(m.time for m in t) for t in mid_in.tracks), default=0)

        # 2. Generate Beat Track (Visual grid/metronome)
        self._create_beat_track(mid_out, total_ticks, mid_in.ticks_per_beat, tempo_events)

        # 3. Build Drums Track
        drum_track = MidiTrack()
        mid_out.tracks.append(drum_track)
        
        # Standard YARG/CH track headers
        for h in ["PART DRUMS", "[mix 0 drums0]", "[play]", "[music_start]"]:
            type_ = "track_name" if "PART" in h else "text"
            kw = "name" if "PART" in h else "text"
            drum_track.append(MetaMessage(type_, **{kw: h}, time=0))

        # Process notes and write to track
        events = self._process_drums(mid_in)
        self._write_track(drum_track, events)

        mid_out.save(output_path)

    def _create_beat_track(self, mid: MidiFile, duration: int, ticks_per_beat: int, tempo_events: List[Tuple[int, MetaMessage]]) -> None:
        """
        Generates the 'BEAT' track used by the game engine for grid alignment.
        """
        track = MidiTrack()
        track.append(MetaMessage("track_name", name="BEAT", time=0))
        mid.tracks.append(track)

        # Default to 4/4 if no signature found
        sigs = [(0, 4)]
        for t, msg in tempo_events:
            if msg.type == "time_signature":
                sigs.append((t, msg.numerator))
        sigs.sort(key=lambda x: x[0])

        curr = 0
        last = 0
        idx = 0
        beats_bar = sigs[0][1]
        beat_count = 0

        # Iterate through every beat in the song
        while curr < duration:
            # Update time signature if we passed a change event
            if idx + 1 < len(sigs) and curr >= sigs[idx + 1][0]:
                idx += 1
                beats_bar = sigs[idx][1]
                beat_count = 0

            # MIDI Note 12 = Downbeat (Bar start), 13 = Standard beat
            note = 12 if beat_count == 0 else 13
            
            track.append(Message("note_on", note=note, velocity=100, time=curr - last, channel=0))
            track.append(Message("note_off", note=note, velocity=0, time=0, channel=0))

            last = curr
            curr += ticks_per_beat
            beat_count = (beat_count + 1) % beats_bar

    def _process_drums(self, mid_in: MidiFile) -> List[Tuple[int, str, int, int]]:
        """
        Extracts relevant drum notes, applies mapping, and handles 
        Tom markers (blue/yellow/green cymbal vs tom distinction).
        """
        timeline = defaultdict(list)
        
        for track in mid_in.tracks:
            abs_t = 0
            for msg in track:
                abs_t += msg.time
                
                if (msg.type == "note_on" and msg.channel == 9):
                    if msg.velocity >= MIN_VELOCITY and msg.note in DRUM_MAPPING:
                        # Store by absolute time to handle simultaneous hits
                        timeline[abs_t].append(msg.note)

        # Remove impossible simultaneous inputs (more than 2 hands + foot)
        self._humanize_timeline(timeline)

        final_events = []
        
        for t in sorted(timeline.keys()):
            raw_notes = set(timeline[t])
            
            for midi_n in raw_notes:
                gem = DRUM_MAPPING[midi_n]
                
                final_events.append((t, "note_on", gem, 100))
                final_events.append((t + NOTE_LEN, "note_off", gem, 0))

                # Add special marker notes if the drum is a Tom
                if midi_n in IS_TOM and gem in TOM_MARKERS_MAP:
                    m = TOM_MARKERS_MAP[gem]
                    final_events.append((t, "note_on", m, 100))
                    final_events.append((t + NOTE_LEN, "note_off", m, 0))

        return sorted(final_events, key=lambda x: x[0])

    def _humanize_timeline(self, timeline: Dict[int, List[int]]) -> None:
        """
        Enforces a 2-hand limit for non-kick drum parts.
        Uses a priority map to decide which notes to keep (e.g. Crash > Hi-Hat).
        """
        # Lower number = Higher priority to keep
        PRIORITY = {
            38: 3, 40: 3, 49: 3, 57: 3,        # Snares / Crashes
            51: 2, 59: 2, 41: 2, 43: 2, 45: 2, # Toms / Rides
            47: 2, 48: 2, 50: 2, 
            42: 1, 44: 1, 46: 1                # Hi-Hats (Usually first to go)
        }
        KICK_NOTES = {35, 36}

        for t, notes in timeline.items():
            unique = list(set(notes))
            if len(unique) <= 2:
                continue

            hands = [n for n in unique if n not in KICK_NOTES]
            feet = [n for n in unique if n in KICK_NOTES]

            # If more than two hands would be required, drop low-priority notes
            if len(hands) > 2:
                hands.sort(key=lambda x: PRIORITY.get(x, 2), reverse=True)
                timeline[t] = feet + hands[:2]

    def _write_track(self, track: MidiTrack, events: List[Tuple[int, str, int, int]]) -> None:
        last_t = 0
        for abs_t, type_, note, vel in events:
            # Calculate delta time relative to the previous event
            delta = max(0, abs_t - last_t)
            track.append(Message(type_, note=note, velocity=vel, time=delta, channel=0))
            last_t = abs_t

    def _create_ini(self, meta: Dict[str, Any], folder: Path) -> None:
        lines = [
            "[song]",
            f"name = {meta.get('name', 'Unknown')}",
            f"artist = {meta.get('artist', 'Unknown')}",
            f"album = {meta.get('album', 'Unknown')}",
            f"genre = {meta.get('genre', 'Rock')}",
            f"year = {meta.get('year', '2025')}",
            f"diff_drums = {meta.get('difficulty', '-1')}",
            "pro_drums = True",
            "diff_band = -1", 
            "diff_guitar = -1", 
            "diff_bass = -1",
            "charter = Midi to YARG Converter",
            "loading_phrase = Auto-generated by the Midi to YARG Converter",
        ]
        (folder / "song.ini").write_text("\n".join(lines), encoding="utf-8")