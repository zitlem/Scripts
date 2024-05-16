#reqirements
#pip install -U openai-whisper

import whisper
import os
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

# Iterate over all files in the current directory and its subdirectories
for root, dirs, files in os.walk('.'):
    for filename in files:
        if is_media_file(filename):
            full_path = os.path.join(root, filename)
            print(f"Transcribing {full_path}...")

            # Transcribe the file with auto language detection
            result = model.transcribe(full_path, task="transcribe")

            # Save the transcription
            transcription_filename = os.path.splitext(full_path)[0] + '.txt'
            with open(transcription_filename, 'w') as file:
                file.write(result["text"])

            print(f"Saved transcription to {transcription_filename}")
