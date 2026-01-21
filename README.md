<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/tu-usuario/midi-to-yarg-converter">
    🎵
  </a>

  <h3 align="center">Midi to YARG Converter</h3>

  <p align="center">
    Automated tool to convert General MIDI files into YARG/Clone Hero playable charts.
    <br />
    <br />
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#setup">Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project started from a simple idea: I wanted to play **Doom songs on drums** in YARG (Yet Another Rhythm Game). Since finding specific **drum charts** for them was quite difficult, and manual charting is a time-consuming process, I decided to automate the conversion from MIDI to game chart.

With the help of **Gemini (AI)**, I built this tool to convert standard MIDI files into playable charts, initially focusing on Drums. The goal is to bridge the gap between listening to a song and playing it, without spending hours in a chart editor.

### Project Goal
While this tool automates the heavy lifting of chart creation, **nothing beats the precision and artistry of a manual charter**. 

The goal of this project is not to replace human charting, but to be an **excellent starting point**. By employing advanced heuristics, it generates a solid, enjoyable, and immediately playable base (especially for Drums). This allows charters to skip the tedious work of placing thousands of notes and focus on refining the details,drastically accelerating the workflow.

### Features
- **Multi-Instrument Support**: converts tracks for **Drums, Guitar (5-lane), and Bass (5-lane)**.
- **Advanced Drum Logic**:
  - **Auto-Humanization**: Enforces strict 2-hand limits.
  - **Conflict Resolution**: Intelligently handles cymbal/tom collisions and "Double Crashes" (e.g., moves one cymbal to a different color to allow 2-handed play).
- **Metadata & Audio Handling**:
  - GUI for full metadata editing (Artist, Album, Difficulties per instrument).
  - **Auto-Calculates Band Difficulty** based on active instruments.
  - Automatically copies and renames your audio file to `song.ogg`, ensuring the folder is ready for YARG drop-in.
- **Beat Track Generation**: automatically creates the tempo map and beat grid.
- **Optional Quantization**: includes a "Auto-Quantize" option (snapping to 1/8 notes) to correct small timing imperfections.
- **Optional Count-in**: includes a "Add 4-Beat Count-in" option to add a count-in section at the beginning of the song.

### Built With

This project is built using Python 3.10 and a modern UI library.

* [![Python][Python.org]][Python-url]
* [![CustomTkinter][CustomTkinter-badge]][CustomTkinter-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

You can run this app by downloading the executable (simplest) or running from source.

### Option A: Executable (Recommended)

1. Go to the [Releases](https://github.com/ImpulseNH/MidiToYARG/releases) page.
2. Download the latest `MidiToYARG.exe`.
3. Run the executable.
   > **Note**: Windows might flag it as "Unknown Publisher". This is normal for unsigned independent apps; click "Run Anyway".

### Option B: From Source (Developers)

If you want to modify the code or run it through Python:

### Prerequisites

* Python 3.10 or higher.

### Setup

1. Clone the repo
   ```sh
   git clone https://github.com/ImpulseNH/MidiToYARG.git
   ```
2. Create a virtual environment
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. Open the application by running `main.py`.
2. Click **"Select .mid"** and choose your General MIDI file.
3. The app will try to auto-fill metadata. Review and edit details.
4. (Optional but recommended) **Select Audio**: Choose your backing track (must be `.ogg`). The app will copy it to the final folder as `song.ogg`.
5. **Configure Instruments**: Set difficulties (0-6) for Drums, Guitar, and Bass. Set to 'Disabled' to exclude an instrument.
6. (Optional) Toggle **"Auto-Quantize"** to snap notes to the nearest 1/8 grid.
7. (Optional) Toggle **"Add 4-Beat Count-in"** to add a count-in section at the beginning of the song.
8. Click **"GENERATE CHART"**.
9. A complete song folder (ready for YARG) will be created in the `output` directory.
10. Move this folder to your game's `songs` directory, scan, and play!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Add support for multitrack songs.
- [ ] Add support for more difficulties (currently defaults to Expert).
- [x] Implement smart quantization to align off-beat notes.
- [x] Add support for other instruments (Guitar, Bass).
- [ ] Add support for Pro Keys / Vocals.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Mido Library](https://mido.readthedocs.io/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [YARG Community](https://yarg.in/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[CustomTkinter-badge]: https://img.shields.io/badge/CustomTkinter-000000?style=for-the-badge&logo=python&logoColor=white
[CustomTkinter-url]: https://github.com/TomSchimansky/CustomTkinter
