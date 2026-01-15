# main.py
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from converter import MidiToYARGConverter

# Visual Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.logic = MidiToYARGConverter()
        self.title("Midi to YARG Converter")
        self.geometry("550x650") # Slightly taller for new fields
        
        self.midi_path = ""
        self.output_dir = os.path.join(os.getcwd(), "output")

        self._init_ui()

    def _init_ui(self):
        # Header
        frame_head = ctk.CTkFrame(self, fg_color="transparent")
        frame_head.pack(pady=15)
        ctk.CTkLabel(frame_head, text="MIDI TO YARG CONVERTER", font=("Impact", 32)).pack()
        ctk.CTkLabel(frame_head, text="Only Expert Drums for now", font=("Arial", 12)).pack()

        # MIDI Selector
        frame_midi = ctk.CTkFrame(self)
        frame_midi.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(frame_midi, text="MIDI File (General MIDI):").pack(anchor="w", padx=10, pady=(10,0))
        
        btn_midi = ctk.CTkButton(frame_midi, text="Select .mid", command=self.load_midi)
        btn_midi.pack(side="left", padx=10, pady=10)
        self.lbl_midi = ctk.CTkLabel(frame_midi, text="---", text_color="gray")
        self.lbl_midi.pack(side="left", pady=10)

        # Metadata
        frame_meta = ctk.CTkFrame(self)
        frame_meta.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(frame_meta, text="Song Information:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(10,5))

        # Grid for alignment
        grid = ctk.CTkFrame(frame_meta, fg_color="transparent")
        grid.pack(fill="x", padx=10, pady=5)
        
        # Labels
        ctk.CTkLabel(grid, text="Artist:", anchor="e").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(grid, text="Song:", anchor="e").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(grid, text="Album:", anchor="e").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(grid, text="Genre:", anchor="e").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(grid, text="Year:", anchor="e").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ctk.CTkLabel(grid, text="Difficulty:", anchor="e").grid(row=5, column=0, padx=5, pady=5, sticky="e")

        # Inputs
        self.entry_artist = ctk.CTkEntry(grid, width=250)
        self.entry_artist.grid(row=0, column=1, padx=5, pady=5)
        
        self.entry_song = ctk.CTkEntry(grid, width=250)
        self.entry_song.grid(row=1, column=1, padx=5, pady=5)
        
        self.entry_album = ctk.CTkEntry(grid, width=250)
        self.entry_album.grid(row=2, column=1, padx=5, pady=5)
        
        self.entry_genre = ctk.CTkEntry(grid, width=250)
        self.entry_genre.insert(0, "Rock") # Default
        self.entry_genre.grid(row=3, column=1, padx=5, pady=5)
        
        self.entry_year = ctk.CTkEntry(grid, width=250)
        self.entry_year.insert(0, "2026") # Default
        self.entry_year.grid(row=4, column=1, padx=5, pady=5)

        # Difficulty Selector
        self.diff_var = ctk.StringVar(value="0")
        self.opt_diff = ctk.CTkOptionMenu(grid, values=["0", "1", "2", "3", "4", "5", "6"], variable=self.diff_var, width=250)
        self.opt_diff.grid(row=5, column=1, padx=5, pady=5)

        # Process Button
        self.btn_run = ctk.CTkButton(self, text="GENERATE CHART", height=50, 
                                     fg_color="#1f538d", font=("Arial", 16, "bold"), 
                                     command=self.run_process)
        self.btn_run.pack(pady=20, padx=20, fill="x")

        # Footer
        ctk.CTkLabel(self, text="IMPORTANT: Manually copy your audio file (song.ogg) to the generated folder.", 
                     text_color="orange", font=("Arial", 11)).pack(side="bottom", pady=15)

    def load_midi(self):
        p = filedialog.askopenfilename(filetypes=[("MIDI Files", "*.mid")])
        if p:
            self.midi_path = p
            self.lbl_midi.configure(text=os.path.basename(p), text_color="white")
            
            # Auto-fill
            base = os.path.splitext(os.path.basename(p))[0]
            if "-" in base:
                parts = base.split("-", 1)
                self.entry_artist.delete(0, "end"); self.entry_artist.insert(0, parts[0].strip())
                self.entry_song.delete(0, "end"); self.entry_song.insert(0, parts[1].strip())
            else:
                self.entry_song.delete(0, "end"); self.entry_song.insert(0, base)
                # Clear if no artist
                if not self.entry_artist.get():
                    self.entry_artist.delete(0, "end"); self.entry_artist.insert(0, "Unknown Artist")

    def run_process(self):
        if not self.midi_path:
            messagebox.showerror("Error", "You must select a MIDI file.")
            return

        # Collect data
        meta = {
            "artist": self.entry_artist.get() or "Unknown Artist",
            "name": self.entry_song.get() or "Unknown Song",
            "album": self.entry_album.get() or "Unknown Album",
            "genre": self.entry_genre.get() or "Rock",
            "year": self.entry_year.get() or "2026",
            "difficulty": self.diff_var.get()
        }

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        try:
            folder = self.logic.process_song(self.midi_path, meta, self.output_dir)
            
            msg = (f"Chart generated successfully!\n\n"
                f"Output folder:\n{folder}\n\n"
                "Next steps:\n"
                "1. Add your audio file (song.ogg).\n"
                "2. Copy the entire folder to your YARG songs directory.\n"
                "3. Launch YARG and play your custom chart.")

            
            messagebox.showinfo("Process Completed", msg)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()