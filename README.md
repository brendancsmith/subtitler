# Video Subtitling Tool

This project provides a set of tools for processing video files, including extracting audio, transcribing audio to text, generating subtitles, and adding subtitles to video files. It uses the whisper library to transcribe audio.

## Installation

### ffmpeg

FFmpeg is required for processing video and audio files. Follow the instructions below to install FFmpeg on your platform.

#### Windows

1. Download the FFmpeg zip file from the [official website](https://ffmpeg.org/download.html).
2. Extract the zip file to a folder of your choice.
3. Add the `bin` folder inside the extracted folder to your system's PATH environment variable.

#### macOS

1. Install Homebrew if you haven't already: 
    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
2. Install FFmpeg using Homebrew:
    ```bash
    brew install ffmpeg
    ```

#### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

### Python Packages

```bash
pip install -r requirements.txt
```

## Usage

To process video files, run `python main.py`. By default, it processes all `.mp4` files in the `video_input` directory. You can also specify a single video file as an argument.

```bash
python main.py [video_file]
```

## Default Directories

- `assets/video_input/`: Input video files (.mp4)
- `assets/video_output/`: Output video files with subtitles (.mp4)
- `assets/audio/`: Directory for extracted audio files (.mp3)
- `assets/subtitles/`: Directory for generated subtitle files (.srt)
- `assets/text/`: Directory for transcribed text files (.txt)

## License

This project is licensed under the MIT License.
