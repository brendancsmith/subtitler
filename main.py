from datetime import timedelta
from pathlib import Path
from typing import Optional
import os
import subprocess
import whisper


def change_filename(input_file: Path, ext: str, path: Optional[Path] = None) -> Path:
    """
    Change the file extension of a given file path and optionally change the directory.

    Args:
        input_file (Path): The input file path.
        ext (str): The new file extension.
        path (Optional[Path]): The new directory path. If not provided, the original directory is used.

    Returns:
        Path: The new file path with the updated extension and optional directory.
    """
    
    return (
        path / f"{input_file.stem}.{ext}"
        if path
        else input_file.with_suffix(f".{ext}")
    )


def extract_audio(video_file, audio_file):
    """
    Extract the audio stream from a video file and save it as a separate audio file.

    Args:
        video_file (Path): The input video file path.
        audio_file (Path): The output audio file path.
    """
    
    p = subprocess.Popen(["ffmpeg",  "-i", video_file, "-q:a", "0", audio_file])
    p.wait()


def transcribe_audio(input_file):
    """
    Transcribe an audio file using the Whisper speech recognition model.

    Args:
        input_file (Path): The path to the input audio file.

    Returns:
        dict: A dictionary containing the transcription result from the Whisper model.
    """
    
    model = whisper.load_model("base")
    result = model.transcribe(str(input_file))

    return result


def write_subtitles(whisper_result, output_file):
    """
    Write the transcription result from the Whisper model to a SubRip (.srt) subtitle file.

    Args:
        whisper_result (dict): The transcription result from the Whisper model, containing segments
            with start and end times, and the corresponding transcribed text.
        output_file (Path): The path to the output SubRip (.srt) subtitle file.
    """

    with open(output_file, 'w', encoding='utf-8') as srtFile:
        for segment in whisper_result['segments']:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000' 
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            subtitle = f"{segment['id']+1}\n" +\
                f"{startTime} --> {endTime}\n" +\
                f"{segment['text']}\n\n"
            srtFile.write(subtitle)

def write_text(whisper_result, output_file):
    """
    Write the transcribed text from the Whisper model to a text file.

    Args:
        whisper_result (dict): The transcription result from the Whisper model, containing the transcribed text.
        output_file (Path): The path to the output text file.
    """
    
    with open(output_file, 'w', encoding='utf-8') as txtFile:
        txtFile.write(whisper_result['text'])


def add_subtitles(video_file, subtitle_file, output_file):
    """
    Add subtitles to a video file using the provided subtitle file.

    Args:
        video_file (Path or str): The path to the input video file.
        subtitle_file (Path or str): The path to the subtitle file in SubRip (.srt) format.
        output_file (Path or str): The path to the output video file with subtitles.
    """
    p = subprocess.Popen(["ffmpeg", "-i", video_file, "-vf", f"subtitles=\"{subtitle_file}\"", output_file])
    p.wait()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        video_files = list(Path("assets/video_input").resolve().glob("*.mp4"))
        audio_path = Path("assets/audio").resolve()
        subtitles_path = Path("assets/subtitles").resolve()
        text_path = Path("assets/text").resolve()
        output_path = Path("assets/video_output").resolve()
    else:
        video_files = [ Path(sys.argv[1]) ]
        audio_path = Path(video_files[0]).parent
        subtitles_path = Path(video_files[0]).parent
        text_path = Path(video_files[0]).parent
        output_path = Path(video_files[0]).parent

    for video_file in video_files:
        output_file = output_path / f"{video_file.stem} [subtitled].mp4"
        if output_file.exists():
            continue

        audio_file = change_filename(video_file, "mp3", audio_path)
        subtitle_file = change_filename(video_file, "srt", subtitles_path)
        text_file = change_filename(video_file, "txt", text_path)

        extract_audio(video_file, audio_file)
        result = transcribe_audio(audio_file)
        write_subtitles(result, subtitle_file)
        write_text(result, text_file)
        
        add_subtitles(video_file, subtitle_file, output_file)
