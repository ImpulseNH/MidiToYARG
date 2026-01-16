import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from mido import Message, MetaMessage, MidiFile, MidiTrack

from mappings import (
    BLUE_CYMBALS, BLUE_GEM, BLUE_TOMS, DRUM_MAPPING, GREEN_CRASHES,
    GREEN_GEM, GREEN_TOMS, IS_TOM, KICK_NOTES, PRIORITY_MAP,
    TOM_MARKERS_MAP, YELLOW_GEM
)


# Config
NOTE_LEN = 1
MIN_VELOCITY = 20


class MidiToYARGConverter:
    """
    Handles the conversion of raw MIDI files into YARG/Clone Hero compatible charts.
    Includes logic for tempo mapping, beat generation, and strict limb-limit humanization.
    """

    def process_song(self, midi_path: str, metadata: Dict[str, Any], output_dir: str, quantize: bool = True) -> str:
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
        self._create_chart(midi_path, str(folder / "notes.mid"), quantize)
        self._create_ini(metadata, folder)

        return str(folder)

    def _clean_name(self, text: str) -> str:
        return "".join(c for c in text if c.isalnum() or c in " -_.").strip()


    def _create_chart(self, input_path: str, output_path: str, quantize: bool) -> None:
        """
        Rebuilds the MIDI structure. Uses Type 1 to allow separate Tempo and Instrument tracks.
        """
        mid_in = MidiFile(input_path)
        # Type 1 is required for multi-track (Tempo Map + Notes)
        mid_out = MidiFile(type=1, ticks_per_beat=mid_in.ticks_per_beat)

        # 1. Build Tempo Map (Track 0)
        tempo_events = self._build_tempo_track(mid_in, mid_out)

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
        events = self._process_drums(mid_in, quantize)
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

    def _build_tempo_track(self, mid_in: MidiFile, mid_out: MidiFile) -> List[Tuple[int, MetaMessage]]:
        """
        Extracts tempo events and builds the Tempo Map track.
        """
        tempo_track = MidiTrack()
        tempo_track.name = "Tempo Map"
        mid_out.tracks.append(tempo_track)

        tempo_events = []
        abs_time = 0
        
        # Flatten track 0 events to absolute time
        for msg in mid_in.tracks[0]:
            abs_time += msg.time
            if msg.type in ("set_tempo", "time_signature"):
                tempo_events.append((abs_time, msg))

        # Write to track
        last_t = 0
        for t, msg in tempo_events:
            tempo_track.append(msg.copy(time=t - last_t))
            last_t = t
            
        return tempo_events

    def _process_drums(self, mid_in: MidiFile, quantize: bool) -> List[Tuple[int, str, int, int]]:
        """
        Orchestrates the drum processing pipeline: Quantize (Optional) -> Humanize -> Conflict Resolve.
        """
        if quantize:
            timeline = self._quantize_events(mid_in)
        else:
            timeline = self._get_raw_events(mid_in)
        self._humanize_timeline(timeline)
        return self._resolve_conflicts(timeline)

    def _quantize_events(self, mid_in: MidiFile) -> Dict[int, List[int]]:
        """
        Reads MIDI tracks and snaps notes to the nearest grid.
        """
        timeline = defaultdict(list)
        tpb = mid_in.ticks_per_beat
        
        # Config: Snap tolerance (11%) and Grid (1/8 notes)
        tolerance_ticks = tpb * 0.11
        anchor_grid = tpb / 2

        for track in mid_in.tracks:
            abs_t = 0
            for msg in track:
                abs_t += msg.time
                if (msg.type == "note_on" and msg.channel == 9):
                    if msg.velocity >= MIN_VELOCITY and msg.note in DRUM_MAPPING:
                        # Magnetic Snap
                        nearest = round(abs_t / anchor_grid) * anchor_grid
                        final_time = int(nearest) if abs(abs_t - nearest) <= tolerance_ticks else abs_t
                        timeline[final_time].append(msg.note)
        return timeline

    def _get_raw_events(self, mid_in: MidiFile) -> Dict[int, List[int]]:
        """
        Reads MIDI tracks and extracts notes without snapping to grid.
        """
        timeline = defaultdict(list)
        
        for track in mid_in.tracks:
            abs_t = 0
            for msg in track:
                abs_t += msg.time
                if (msg.type == "note_on" and msg.channel == 9):
                    if msg.velocity >= MIN_VELOCITY and msg.note in DRUM_MAPPING:
                        timeline[abs_t].append(msg.note)
        return timeline

    def _resolve_conflicts(self, timeline: Dict[int, List[int]]) -> List[Tuple[int, str, int, int]]:
        """
        Converts timeline to events and resolves color collisions.
        Logic: If a cymbal and a tom share the same color at the same time, 
        one is moved to prevent unplayable gems (e.g., Green Crash vs Green Tom).
        """
        final_events = []

        for t in sorted(timeline.keys()):
            raw_notes = set(timeline[t])
            
            # Check Collisions
            collision_green = not raw_notes.isdisjoint(GREEN_CRASHES) and not raw_notes.isdisjoint(GREEN_TOMS)
            collision_blue = not raw_notes.isdisjoint(BLUE_CYMBALS) and not raw_notes.isdisjoint(BLUE_TOMS)

            for midi_n in raw_notes:
                gem = DRUM_MAPPING[midi_n]
                
                # logic: Move Cymbal if collision exists
                if collision_green and midi_n in GREEN_CRASHES:
                    gem = BLUE_GEM 
                elif collision_blue and midi_n in BLUE_CYMBALS:
                    gem = GREEN_GEM

                # Write Note
                final_events.append((t, "note_on", gem, 100))
                final_events.append((t + NOTE_LEN, "note_off", gem, 0))

                # Write Tom Marker
                if midi_n in IS_TOM and gem in TOM_MARKERS_MAP:
                    marker = TOM_MARKERS_MAP[gem]
                    final_events.append((t, "note_on", marker, 100))
                    final_events.append((t + NOTE_LEN, "note_off", marker, 0))

        return sorted(final_events, key=lambda x: x[0])

    def _humanize_timeline(self, timeline: Dict[int, List[int]]) -> None:
        """
        Enforces 2-hand limit. Kicks are ignored (feet).
        Priority: Snare/Crash (3) > Tom/Ride (2) > Hi-Hat (1).
        """
        for t, notes in timeline.items():
            unique_notes = list(set(notes))
            
            # No optimization needed for feasible hits
            if len(unique_notes) <= 2:
                continue

            hands = [n for n in unique_notes if n not in KICK_NOTES]
            feet = [n for n in unique_notes if n in KICK_NOTES]

            if len(hands) > 2:
                # Sort descending: highest priority remains at index 0 and 1
                hands.sort(key=lambda x: PRIORITY_MAP.get(x, 2), reverse=True)
                
                # Keep top 2 hands + all feet
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