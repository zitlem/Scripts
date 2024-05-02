#reqirements
#pip install -U openai-whisper

import whisper
import os

# Load the Whisper model
model = whisper.load_model("large-v3")


# Function to check if the file is an audio/video file
def is_media_file(filename):
    media_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.mp4', '.mkv', '.avi', '.mov']
    return any(filename.lower().endswith(ext) for ext in media_extensions)

# Iterate over all files in the current directory
for filename in os.listdir('.'):
    if is_media_file(filename):
        print(f"Transcribing {filename}...")

        # Transcribe the file
        result = model.transcribe(filename, language="en", task="transcribe")

        # Save the transcription
        transcription_filename = os.path.splitext(filename)[0] + '.txt'
        with open(transcription_filename, 'w') as file:
            file.write(result["text"])

        print(f"Saved transcription to {transcription_filename}")