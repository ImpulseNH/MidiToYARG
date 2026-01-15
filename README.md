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

This project started from a simple goal: playing Doom songs in YARG (Yet Another Rhythm Game). Since very few charts were available, and manual charting is a time-consuming process, I decided to automate it.

With the help of **Gemini (AI)**, I built this tool to convert standard MIDI files into playable charts, initially focusing on Drums. The goal is to bridge the gap between listening to a song and playing it, without spending hours in a chart editor.


### Features
- **MIDI to Chart Conversion**: automatically converts `.mid` files to `notes.mid` compatible with YARG and Clone Hero.
- **Auto-Humanization**: includes a smart logic to enforce a 2-hand limit, filtering out impossible inputs (e.g., removing a 3rd concurrent hand hit while keeping the kick drum).
- **Metadata Management**: easy-to-use GUI to input song details (Artist, Album, Year, etc.) which generates the `song.ini` file.
- **Beat Track Generation**: automatically creates the tempo map and beat grid for the game engine.

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
3. The app will try to auto-fill metadata from the filename. Review and edit the fields (Artist, Song, Genre, Difficulty).
4. Click **"GENERATE CHART"**.
5. A folder will be created in the `output` directory.
6. **Important**: You must manually copy your audio file (renamed to `song.ogg`) into this new folder.
7. Move the entire folder to your YARG/Clone Hero `songs` directory.
8. Rescan songs in-game and play!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Add support for more difficulties (currently defaults to Expert).
- [ ] Implement smart quantization to align off-beat notes.
- [ ] Add support for other instruments (Guitar, Bass).

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
