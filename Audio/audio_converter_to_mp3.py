import os
import ffmpeg
from tqdm import tqdm
from pydub.utils import mediainfo

def convert_to_mp3_ffmpeg(audio_file, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Define output file path
    output_file = os.path.join(output_folder, os.path.splitext(audio_file)[0] + ".mp3")

    # Extract metadata from the original file
    metadata = mediainfo(audio_file)
    
    # Convert audio to MP3 while explicitly preserving metadata
    try:
        (
            ffmpeg
            .input(audio_file)
            .output(output_file, **{"q:a": 2}, map_metadata="0")  # Ensures metadata is copied
            .run(overwrite_output=True, quiet=True)
        )
        return f"Converted {audio_file} to {output_file} with metadata preserved"
    except Exception as e:
        return f"Error converting {audio_file}: {e}"

def find_audio_files_and_convert():
    # Specify the output folder
    output_folder = "output_folder"
    
    # Get the list of files in the current directory
    files_in_directory = os.listdir()
    
    # Supported audio file extensions
    supported_extensions = ('.wav', '.flac', '.ogg', '.aac', '.m4a', '.opus', '.mp4')
    
    # Filter the files to only include supported audio files
    audio_files = [file for file in files_in_directory if file.endswith(supported_extensions)]
    
    # Overall progress bar for the whole process
    with tqdm(total=len(audio_files), desc="Converting files", unit="file") as pbar:
        # Iterate over the audio files and convert them
        for audio_file in audio_files:
            result = convert_to_mp3_ffmpeg(audio_file, output_folder)
            pbar.set_postfix_str(result)
            pbar.update(1)

if __name__ == "__main__":
    find_audio_files_and_convert()
