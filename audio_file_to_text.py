#reqirements
#pip install -U openai-whisper

import whisper
import os
import time
import warnings

# Suppress the UserWarning about FP16 not supported on CPU
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Load the Whisper model, defaulting to CPU if GPU is not available
try:
    model = whisper.load_model("large-v3", device="gpu")
except RuntimeError:
    print("GPU not available. Using CPU instead.")
    model = whisper.load_model("large-v3", device="cpu")

# Function to check if the file is an audio/video file
def is_media_file(filename):
    media_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.mp4', '.mkv', '.avi', '.mov']
    return any(filename.lower().endswith(ext) for ext in media_extensions)

# Function to format time in seconds to hours, minutes, and seconds
def format_time(seconds):
    hours = int(seconds) // 3600
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return hours, minutes, seconds

# Function to format time to HH:MM:SS format
def format_time_string(hours, minutes, seconds):
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# Iterate over all files in the current directory and its subdirectories
total_start_time = time.time()
for root, dirs, files in os.walk('.'):
    for filename in files:
        if is_media_file(filename):
            full_path = os.path.join(root, filename)
            print(f"Transcribing {full_path}...")
            start_time = time.time()

            # Transcribe the file with auto language detection
            result = model.transcribe(full_path, task="transcribe")

            # Save the transcription with timestamps
            transcription_filename = os.path.splitext(full_path)[0] + '_transcript.txt'
            with open(transcription_filename, 'w', encoding='utf-8') as file:
                for segment in result["segments"]:
                    start_time_formatted = format_time(segment["start"])
                    end_time_formatted = format_time(segment["end"])
                    text = segment["text"]
                    file.write(f"{format_time_string(*start_time_formatted)} --> {format_time_string(*end_time_formatted)}\n{text}\n\n")

            end_time = time.time()
            duration = end_time - start_time
            duration_hours, duration_minutes, duration_seconds = format_time(duration)
            print(f"Saved transcription to {transcription_filename}. Duration: {duration_hours} hours, {duration_minutes} minutes, {duration_seconds} seconds")

total_end_time = time.time()
total_duration = total_end_time - total_start_time
total_duration_hours, total_duration_minutes, total_duration_seconds = format_time(total_duration)
print(f"Total transcription duration: {total_duration_hours} hours, {total_duration_minutes} minutes, {total_duration_seconds} seconds")