import os
import webbrowser
from tkinter import filedialog, messagebox

import customtkinter as ctk

from converter import MidiToYARGConverter


# Configuration
VERSION = "0.2.0-beta"
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
        self.geometry("550x700")
        
        self.midi_path = ""
        self.output_dir = os.path.join(os.getcwd(), "output")

    def _init_ui(self):
        """Construct the user interface."""
        self._create_header()
        self._create_midi_selector()
        self._create_metadata_form()
        self._create_action_section()
        self._create_footer()

    def _create_header(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=15)
        
        # Title
        ctk.CTkLabel(frame, text="MIDI TO YARG", font=("Impact", 32)).pack()
        # Subtitle
        ctk.CTkLabel(frame, text="Expert Drums Converter", font=("Arial", 12)).pack()
        # Version
        ctk.CTkLabel(frame, text=f"v{VERSION}", font=("Arial", 10), text_color="gray").pack(pady=(2,0))

    def _create_midi_selector(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(frame, text="Source MIDI File:").pack(anchor="w", padx=10, pady=(10,0))
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkButton(btn_frame, text="Browse .mid", command=self._select_midi_file, width=100).pack(side="left")
        self.lbl_filename = ctk.CTkLabel(btn_frame, text="No file selected", text_color="gray")
        self.lbl_filename.pack(side="left", padx=10)

    def _create_metadata_form(self):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(frame, text="Song Details:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        
        self.form_entries = {}
        fields = [
            ("Artist", "Unknown Artist"),
            ("Song", "Unknown Song"),
            ("Album", "Unknown Album"),
            ("Genre", "Rock"),
            ("Year", "2026")
        ]

        grid = ctk.CTkFrame(frame, fg_color="transparent")
        grid.pack(fill="x", padx=10, pady=5)

        for i, (label_text, default_val) in enumerate(fields):
            ctk.CTkLabel(grid, text=f"{label_text}:", anchor="e").grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ctk.CTkEntry(grid, width=250)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, default_val)
            self.form_entries[label_text.lower()] = entry

        # Difficulty Selector
        ctk.CTkLabel(grid, text="Difficulty:", anchor="e").grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.diff_var = ctk.StringVar(value="0")
        ctk.CTkOptionMenu(grid, values=[str(x) for x in range(7)], variable=self.diff_var, width=250).grid(row=5, column=1, padx=5, pady=5)
        
        # Quantization Switch
        self.quantize_var = ctk.BooleanVar(value=False)
        sw = ctk.CTkSwitch(grid, text="Auto-Quantize", variable=self.quantize_var, onvalue=True, offvalue=False)
        sw.grid(row=6, column=1, padx=5, pady=10, sticky="w")
        
        # Add Tooltip
        tooltip_text = (
            "Tries to correct any imperfections the song may have.\n\n"
            "Warning: This may not be perfectly accurate.\n"
            "If the result is imprecise, consider using Moonscraper Chart Editor "
            "after converting the song."
        )
        moonscraper_url = "https://github.com/FireFox2000000/Moonscraper-Chart-Editor"
        CTkToolTip(sw, text=tooltip_text, url=moonscraper_url)

    def _create_action_section(self):
        self.btn_run = ctk.CTkButton(self, text="GENERATE CHART", height=50, 
                                     fg_color="#1f538d", font=("Arial", 16, "bold"), 
                                     command=self._process_chart)
        self.btn_run.pack(pady=20, padx=20, fill="x")

    def _create_footer(self):
        info_text = "IMPORTANT: Copy your 'song.ogg' manually to the output folder."
        ctk.CTkLabel(self, text=info_text, text_color="orange", font=("Arial", 11)).pack(side="bottom", pady=15)

    def _select_midi_file(self):
        path = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if path:
            self.midi_path = path
            filename = os.path.basename(path)
            self.lbl_filename.configure(text=filename, text_color="white")
            self._fill_metadata_from_filename(filename)

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
        data['difficulty'] = self.diff_var.get()
        return data

    def _process_chart(self):
        if not self.midi_path:
            messagebox.showerror("Error", "Please select a MIDI file first.")
            return

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            meta = self._get_form_data()
            quantize = self.quantize_var.get()
            folder = self.converter.process_song(self.midi_path, meta, self.output_dir, quantize=quantize)
            
            msg = (f"Chart generated successfully!\n\n"
                   f"Output Location:\n{folder}\n\n"
                   "Next Step: Add your audio file (song.ogg) to this folder.")
            
            messagebox.showinfo("Success", msg)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()