import os
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk

from converter import MidiToYARGConverter


# Configuration
VERSION = "1.0.0"
THEME_MODE = "Dark"
THEME_COLOR = "blue"


class CTkToolTip(ctk.CTkToplevel):
    def __init__(self, widget, text, url=None):
        super().__init__()
        self.widget = widget
        self.text = text
        self.url = url
        self.withdraw()
        self.overrideredirect(True)
        
        self.label = ctk.CTkLabel(self, text=self.text, fg_color="#333333", text_color="white", corner_radius=6, padx=10, pady=5)
        self.label.pack()
        
        if self.url:
            self.label.configure(cursor="hand2")
            self.label.bind("<Button-1>", lambda e: webbrowser.open_new_tab(self.url))
            self.label.configure(text=f"{self.text}\n\n(Click to open Moonscraper)")
        
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
        
        # Interactivity: don't hide if mouse is over tooltip
        self.bind("<Enter>", lambda e: self.show_tooltip())
        self.bind("<Leave>", lambda e: self.hide_tooltip())
        
    def show_tooltip(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + 30
        self.geometry(f"+{x}+{y}")
        self.deiconify()
        self.lift()
        
    def hide_tooltip(self, event=None):
        # Small delay to check if we moved to the tooltip itself
        self.after(100, self._check_hide)

    def _check_hide(self):
        # Hide if mouse is not over widget and not over tooltip
        x, y = self.winfo_pointerxy()
        widget_x1 = self.widget.winfo_rootx()
        widget_x2 = widget_x1 + self.widget.winfo_width()
        widget_y1 = self.widget.winfo_rooty()
        widget_y2 = widget_y1 + self.widget.winfo_height()
        
        over_widget = (widget_x1 <= x <= widget_x2) and (widget_y1 <= y <= widget_y2)
        
        tooltip_x1 = self.winfo_rootx()
        tooltip_x2 = tooltip_x1 + self.winfo_width()
        tooltip_y1 = self.winfo_rooty()
        tooltip_y2 = tooltip_y1 + self.winfo_height()
        
        over_tooltip = (tooltip_x1 <= x <= tooltip_x2) and (tooltip_y1 <= y <= tooltip_y2)
        
        if not over_widget and not over_tooltip:
            self.withdraw()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.converter = MidiToYARGConverter()
        self._setup_window()
        self._init_ui()

    def _setup_window(self):
        """Configure main window properties and theme."""
        ctk.set_appearance_mode(THEME_MODE)
        ctk.set_default_color_theme(THEME_COLOR)
        
        self.title(f"Midi to YARG Converter {VERSION}")
        self.geometry("800x750")
        self.resizable(False, False)
        
        self.midi_path = ""
        self.output_dir = os.path.join(os.getcwd(), "output")

    def _init_ui(self):
        """Construct the user interface."""
        self._create_header()
        self._create_file_inputs()
        self._create_metadata_form()
        self._create_action_section()
        self._create_footer()

    def _create_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=15)
        
        # Title
        ctk.CTkLabel(frame, text="MIDI TO YARG", font=("Impact", 32)).pack()
        # Subtitle
        ctk.CTkLabel(frame, text="Multi-Instrument Chart Converter", font=("Arial", 12)).pack()
        # Version
        ctk.CTkLabel(frame, text=f"v{VERSION}", font=("Arial", 10), text_color="gray").pack(pady=(2,0))



    def _create_file_inputs(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, padx=20, fill="x")

        # Title
        ctk.CTkLabel(frame, text="File Selection", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        # Grid for file inputs
        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x", padx=10, pady=5)
        
        # 1. Source MIDI
        ctk.CTkLabel(grid, text="Source MIDI:", anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.lbl_midi = ctk.CTkLabel(grid, text="No file selected", text_color="gray", width=300, anchor="w")
        self.lbl_midi.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(grid, text="Browse", width=80, command=self._select_midi_file).grid(row=0, column=2, padx=5, pady=5)

        # 2. Audio File
        ctk.CTkLabel(grid, text="Song Audio:", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.lbl_audio = ctk.CTkLabel(grid, text="Optional (song.ogg)", text_color="gray", width=300, anchor="w")
        self.lbl_audio.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(grid, text="Browse", width=80, command=self._select_audio_file).grid(row=1, column=2, padx=5, pady=5)

        # 3. Output Folder
        ctk.CTkLabel(grid, text="Output Dir:", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.lbl_output = ctk.CTkLabel(grid, text=self.output_dir, text_color="white", width=300, anchor="w")
        self.lbl_output.grid(row=2, column=1, padx=5, pady=5)
        ctk.CTkButton(grid, text="Browse", width=80, command=self._select_output_dir).grid(row=2, column=2, padx=5, pady=5)

        self.audio_path = ""

    def _create_metadata_form(self):
        # --- TOP SECTION: Metadata & Instruments ---
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(pady=10, padx=20, fill="x")
        
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)

        # 1. Left Column: Metadata
        left_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10)

        ctk.CTkLabel(left_frame, text="Song Details", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))

        self.form_entries = {}
        fields = [
            ("Artist", "Unknown Artist"),
            ("Song", "Unknown Song"),
            ("Album", "Unknown Album"),
            ("Genre", "Rock"),
            ("Year", "2026")
        ]
        
        meta_grid = ctk.CTkFrame(left_frame, fg_color="transparent")
        meta_grid.pack(fill="x")

        for i, (label_text, default_val) in enumerate(fields):
            ctk.CTkLabel(meta_grid, text=f"{label_text}:", anchor="w").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entry = ctk.CTkEntry(meta_grid, width=200)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="e")
            entry.insert(0, default_val)
            self.form_entries[label_text.lower()] = entry

        # 2. Right Column: Instruments & Difficulty Matrix
        right_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(right_frame, text="Instruments Setup", font=("Arial", 14, "bold")).pack(anchor="w", pady=(0, 10))
        
        # Auto-Detect Checkbox
        self.auto_detect_var = ctk.BooleanVar(value=True)
        self.cb_auto = ctk.CTkCheckBox(right_frame, text="Auto-Detect Tracks", variable=self.auto_detect_var, command=self._toggle_track_selectors)
        self.cb_auto.pack(anchor="w", pady=(0, 10))

        # Matrix Grid
        matrix_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        matrix_frame.pack(fill="x")
        
        # Headers
        ctk.CTkLabel(matrix_frame, text="Instrument", text_color="gray70", font=("Arial", 11)).grid(row=0, column=0, padx=5, sticky="w")
        ctk.CTkLabel(matrix_frame, text="Source Track", text_color="gray70", font=("Arial", 11)).grid(row=0, column=1, padx=5, sticky="w")
        ctk.CTkLabel(matrix_frame, text="Difficulty", text_color="gray70", font=("Arial", 11)).grid(row=0, column=2, padx=5, sticky="w")
        
        self.diff_vars = {}
        # Disabled + 0-6
        diff_values = ["Disabled"] + [str(x) for x in range(7)] 

        # -- Drums Row --
        ctk.CTkLabel(matrix_frame, text="Drums:", anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ctk.CTkLabel(matrix_frame, text="Auto (Channel 10)", text_color="gray").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        self.diff_vars['drums'] = ctk.StringVar(value="6") # Default Expert
        ctk.CTkOptionMenu(matrix_frame, values=diff_values, variable=self.diff_vars['drums'], width=110).grid(row=1, column=2, padx=5, pady=5)

        # -- Guitar Row --
        ctk.CTkLabel(matrix_frame, text="Guitar:", anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cbo_guitar = ctk.CTkOptionMenu(matrix_frame, values=["Load MIDI first"], state="disabled", width=140)
        self.cbo_guitar.grid(row=2, column=1, padx=5, pady=5)
        
        self.diff_vars['guitar'] = ctk.StringVar(value="6")
        ctk.CTkOptionMenu(matrix_frame, values=diff_values, variable=self.diff_vars['guitar'], width=110).grid(row=2, column=2, padx=5, pady=5)

        # -- Bass Row --
        ctk.CTkLabel(matrix_frame, text="Bass:", anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cbo_bass = ctk.CTkOptionMenu(matrix_frame, values=["Load MIDI first"], state="disabled", width=140)
        self.cbo_bass.grid(row=3, column=1, padx=5, pady=5)
        
        self.diff_vars['bass'] = ctk.StringVar(value="6")
        ctk.CTkOptionMenu(matrix_frame, values=diff_values, variable=self.diff_vars['bass'], width=110).grid(row=3, column=2, padx=5, pady=5)

        # Note Label
        inst_label = ctk.CTkLabel(matrix_frame, text="Note: Set to 'Disabled' to turn off an instrument.", text_color="gray", font=("Arial", 10))
        inst_label.grid(row=4, column=0, columnspan=3, pady=(5, 0), sticky="w")


        # --- BOTTOM SECTION: Options ---
        opts_frame = ctk.CTkFrame(self, fg_color="transparent")
        opts_frame.pack(pady=5, padx=20, fill="x")

        # Separator
        ctk.CTkFrame(opts_frame, height=2, fg_color="gray50").pack(fill="x", pady=10)
        ctk.CTkLabel(opts_frame, text="Advanced Options", font=("Arial", 12, "bold")).pack(pady=(0,5))
        
        # Switches Container (Centered)
        sw_container = ctk.CTkFrame(opts_frame, fg_color="transparent")
        sw_container.pack()

        # Quantize
        self.quantize_var = ctk.BooleanVar(value=True)
        sw_quant = ctk.CTkSwitch(sw_container, text="Auto-Quantize", variable=self.quantize_var, onvalue=True, offvalue=False)
        sw_quant.pack(side="left", padx=20)
        
        tooltip_text = "Tries to fix timing imperfections.\nIf inaccurate, adjust with Moonscraper after converting."
        moonscraper_url = "https://github.com/FireFox2000000/Moonscraper-Chart-Editor"
        CTkToolTip(sw_quant, text=tooltip_text, url=moonscraper_url)

        # Ghosts
        self.ghosts_var = ctk.BooleanVar(value=False)
        sw_ghost = ctk.CTkSwitch(sw_container, text="Include Ghost Notes", variable=self.ghosts_var, onvalue=True, offvalue=False)
        sw_ghost.pack(side="left", padx=20)

    def _toggle_track_selectors(self):
        state = "disabled" if self.auto_detect_var.get() else "normal"
        self.cbo_guitar.configure(state=state)
        self.cbo_bass.configure(state=state)

    def _create_action_section(self):
        self.btn_run = ctk.CTkButton(self, text="GENERATE CHART", height=50, 
                                     fg_color="#1f538d", font=("Arial", 16, "bold"), 
                                     command=self._process_chart)
        self.btn_run.pack(pady=20, padx=20, fill="x")

    def _create_footer(self):
        # Footer simplified since instructions are clearer now
        pass

    def _select_midi_file(self):
        path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if path:
            self.midi_path = path
            filename = os.path.basename(path)
            self.lbl_midi.configure(text=filename, text_color="white")
            self._fill_metadata_from_filename(filename)
            
            # Scan tracks
            track_list = self.converter.scan_tracks(path)
            if not track_list:
                track_list = ["No tracks found"]
            
            # Add 'None' option
            options = ["None"] + track_list
            
            self.cbo_guitar.configure(values=options)
            self.cbo_bass.configure(values=options)
            self.cbo_guitar.set("None")
            self.cbo_bass.set("None")

    def _select_audio_file(self):
        path = filedialog.askopenfilename(filetypes=[("OGG Files", "*.ogg"), ("All Files", "*.*")])
        if path:
            if not path.lower().endswith(".ogg"):
                messagebox.showwarning("Warning", "Selected file is not .ogg. Rhythm games require .ogg for proper compatibility.")
            
            self.audio_path = path
            filename = os.path.basename(path)
            self.lbl_audio.configure(text=filename, text_color="white")

    def _select_output_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.output_dir = path
            self.lbl_output.configure(text=path, text_color="white")

    def _fill_metadata_from_filename(self, filename):
        """Auto-populate Artist and Song fields based on filename pattern 'Artist - Song'."""
        base = os.path.splitext(filename)[0]
        artist_entry = self.form_entries['artist']
        song_entry = self.form_entries['song']
        
        # Clear current values
        artist_entry.delete(0, "end")
        song_entry.delete(0, "end")

        if "-" in base:
            parts = base.split("-", 1)
            artist_entry.insert(0, parts[0].strip())
            song_entry.insert(0, parts[1].strip())
        else:
            artist_entry.insert(0, "Unknown Artist")
            song_entry.insert(0, base)

    def _get_form_data(self):
        data = {key: entry.get() for key, entry in self.form_entries.items()}
        # Rename 'song' to 'name' as expected by converter
        data['name'] = data.pop('song')
        
        # Parse difficulties
        def parse_diff(val_str):
            if "Disabled" in val_str:
                return -1
            try:
                return int(val_str)
            except ValueError:
                return 0

        d_drums = parse_diff(self.diff_vars['drums'].get())
        d_guitar = parse_diff(self.diff_vars['guitar'].get())
        d_bass = parse_diff(self.diff_vars['bass'].get())

        data['diff_drums'] = str(d_drums)
        data['diff_guitar'] = str(d_guitar)
        data['diff_bass'] = str(d_bass)

        # Calculate Band Difficulty (Average of active instruments)
        # Instrument is active if difficulty >= 0
        active_diffs = []
        if d_drums >= 0: active_diffs.append(d_drums)
        if d_guitar >= 0: active_diffs.append(d_guitar)
        if d_bass >= 0: active_diffs.append(d_bass)
        
        if active_diffs:
            avg = sum(active_diffs) / len(active_diffs)
            data['diff_band'] = str(round(avg))
        else:
            # If all are disabled
            data['diff_band'] = "-1"
            
        return data

    def _process_chart(self):
        if not self.midi_path:
            messagebox.showerror("Error", "Please select a MIDI file first.")
            return
            
        if not self.audio_path:
            confirm = messagebox.askyesno("Missing Audio", "No audio file selected. The chart will be generated without audio.\n\nContinue anyway?")
            if not confirm:
                return
        elif not self.audio_path.lower().endswith(".ogg"):
            messagebox.showerror("Error", "Invalid audio format. Please select an .ogg file or leave it empty.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Get data early to check folder existence
        meta = self._get_form_data()
        
        # Check for existing folder to prompt overwrite
        def clean_name_check(text):
             return "".join(c for c in text if c.isalnum() or c in " -_.").strip()

        artist = clean_name_check(meta.get("artist", "Unknown"))
        song = clean_name_check(meta.get("name", "Untitled"))
        folder_name = f"{artist} - {song}"
        target_path = os.path.join(self.output_dir, folder_name)

        if os.path.exists(target_path):
            confirm = messagebox.askyesno("Overwrite Warning", f"Folder '{folder_name}' already exists.\n\nFiles will be merged/overwritten.\nExisting images/audio will be preserved unless replaced.\n\nContinue?")
            if not confirm:
                return

        try:
            # meta is already retrieved
            quantize = self.quantize_var.get()
            ghosts = self.ghosts_var.get()
            
            # Instrument Overrides
            bass_idx_ovr = -1
            guitar_idx_ovr = -1
            
            if not self.auto_detect_var.get():
                # Helper to extract index from string "2: Track Name"
                def get_idx(val):
                    if not val or val == "None": return -1
                    try:
                        return int(val.split(":")[0])
                    except:
                        return -1
                
                bass_idx_ovr = get_idx(self.cbo_bass.get())
                guitar_idx_ovr = get_idx(self.cbo_guitar.get())

            folder = self.converter.process_song(
                self.midi_path, meta, self.output_dir, 
                quantize=quantize, include_ghosts=ghosts,
                bass_idx=bass_idx_ovr, guitar_idx=guitar_idx_ovr,
                audio_path=self.audio_path
            )
            
            msg = (f"Chart generated successfully!\n\n"
                   f"Output Location:\n{folder}\n\n"
                   "Next Step: Add your audio file (song.ogg) to this folder.")
            
            messagebox.showinfo("Success", msg)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()