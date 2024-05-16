import os
from pydub import AudioSegment
from tqdm import tqdm

def convert_to_mp3(audio_file, output_folder):
    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_file)
    
    # Create the output MP3 file name in the output_folder
    output_file = os.path.join(output_folder, os.path.splitext(audio_file)[0] + ".mp3")
    
    # Export the audio as MP3
    audio.export(output_file, format="mp3")
    
    return f"Converted {audio_file} to {output_file}"

def find_audio_files_and_convert():
    # Specify the output folder
    output_folder = "output_folder"
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get the list of files in the current directory
    files_in_directory = os.listdir()
    
    # Supported audio file extensions (you can add more if needed)
    supported_extensions = ('.wav', '.flac', '.ogg', '.aac', '.m4a','.opus')
    
    # Filter the files to only include supported audio files
    audio_files = [file for file in files_in_directory if file.endswith(supported_extensions)]
    
    # Overall progress bar for the whole process
    with tqdm(total=len(audio_files), desc="Converting files", unit="file") as pbar:
        # Iterate over the audio files and convert them
        for audio_file in audio_files:
            result = convert_to_mp3(audio_file, output_folder)
            pbar.set_postfix_str(result)
            pbar.update(1)

if __name__ == "__main__":
    find_audio_files_and_convert()
