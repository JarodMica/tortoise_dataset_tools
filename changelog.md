# Changelog

## 3/22/2024
- pydub was causing issues for large files larger than 4gb so switched back over to calling ffmpeg from subprocess inside of dataset_maker_large_files.py
    - Also made it default to convert to mp3 and it's done before srt transcription

## 3/19/2024
- Some compatibility changes for paramters within dataset_maker_large_files were made in order to be compatible with AI Voice Cloning repo
    - Modified the default sample rate to downsample to 22050hz for segments after transcription