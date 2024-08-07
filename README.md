# YouTube Remix Script

This Python project facilitates the creation of music remixes by applying various audio effects to MP3 files sourced from YouTube videos. It provides functionalities for downloading YouTube videos, extracting audio, and applying customizable effects like speed adjustment, pitch shift, and more.

## Prerequisites

- Python 3.x installed on your system.
- A code editor software (like VSCode).

## Usage

There are two scripts in this project: `remix_script_menu.py` and `remix_script.py`.

### `remix_script_menu.py`

This script provides an interactive menu to guide users through downloading YouTube videos and applying audio effects.

#### Steps to Use

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/FireEmblem59/audio-modification.git
   cd audio-modification
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Script:**
   ```sh
   python remix_script_menu.py
   ```

4. **Interactive Menu:**
   - Select an option from the menu to download and convert a YouTube video, apply effects to an existing MP3 file, view help, or exit.

### `remix_script.py`

This script allows users to apply audio effects directly via command-line arguments without the interactive menu.

#### Steps to Use

1. **Clone the Repository:**
   ```sh
   git clone https://github.com/FireEmblem59/audio-modification.git
   cd audio-modification
   ```

2. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Script:**
   ```sh
   python remix_script.py [-h] [-o OUTPUT_NAME] [-a AUDIO_INPUT] [-u YOUTUBE_URL]
                          [-s SPEED_RATIO] [-p PITCH_SHIFT] [-l LOWPASS_CUTOFF]
                          [-b BASS_BOOST] [-ga GAIN_DB] [-op] [-ph] [-tr] [-co] [-nr]
                          [-e {slowed_reversed,sped_up,keep_original}]
   ```

## Arguments

- `-o, --output OUTPUT_NAME`: Name of the output file.
- `-a, --audio AUDIO_INPUT`: Input audio file to modify (.mp3).
- `-u, --url YOUTUBE_URL`: YouTube URL to download and remix.
- `-s, --speed SPEED_RATIO`: Ratio of new playback speed to old speed.
- `-p, --pitch PITCH_SHIFT`: Pitch shift (100ths of a semitone).
- `-l, --lowpass LOWPASS_CUTOFF`: Cutoff for lowpass filter (Hz).
- `-b, --bass BASS_BOOST`: Add a bass boost effect.
- `-ga, --gain GAIN_DB`: Apply gain (dB).
- `-op, --oops`: Apply Out Of Phase Stereo effect.
- `-ph, --phaser`: Enable phaser effect.
- `-tr, --tremolo`: Enable tremolo effect.
- `-co, --compand`: Enable compand, which compresses the dynamic range of the audio.
- `-nr, --noreverb`: Disable reverb.
- `-e, --effect {slowed_reversed,sped_up,keep_original}`: Choose audio effect.

## Examples

### Using `remix_script_menu.py`

1. **Run the Interactive Script:**
   ```sh
   python remix_script_menu.py
   ```

### Using `remix_script.py`

1. **Download a YouTube video and apply slowed and reversed effect:**
   ```sh
   python remix_script.py -u <youtube_url> -e slowed_reversed
   ```

2. **Remix an existing audio file with custom effects:**
   ```sh
   python remix_script.py -a <audio_file.mp3> -s 1.2 -p -25 -l 5000 -b 5 -ga 3 -ph -tr
   ```

## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
