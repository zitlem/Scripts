import os
import subprocess

# Function to handle user input for overwriting files
def handle_overwrite_prompt(file_path):
    while True:
        user_input = input(f"File {file_path} already exists. Do you want to overwrite (O) or skip (S)? (O/S): ").strip().lower()
        if user_input in {'o', 's'}:
            return user_input

# Function to find video files recursively based on specified extensions
def find_video_files(root_folder, extensions):
    video_files = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(extensions):
                video_files.append(os.path.join(root, file))

    return video_files

# Function to find VIDEO_TS folders recursively
def find_video_ts_folders(root_folder):
    video_ts_folders = []

    for root, dirs, files in os.walk(root_folder):
        if 'VIDEO_TS.IFO' in files:
            video_ts_folders.append(root)

    return video_ts_folders

# Function to find AVCHD folders recursively (only based on 'BDMV' directory)
def find_avchd_folders(root_folder):
    avchd_folders = []

    for root, dirs, files in os.walk(root_folder):
        if 'BDMV' in dirs:
            avchd_folders.append(root)

    return avchd_folders





def get_output_format():
    while True:
        print("Select an output format:")
        output_formats = [
            '.webm', '.avi', '.mkv', '.mov', '.ts', '.3gp', '.mxf', '.asf', '.flv',
            '.mp4', '.mpeg', '.mpg', '.wmv'
        ]
        output_formats.sort()  # Sort the output formats alphabetically
        for i, format in enumerate(output_formats, start=1):
            print(f"{i}. {format}")
        print(f"{len(output_formats) + 1}. All available formats")

        choice = input("Enter the number of the desired format: ")

        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(output_formats) + 1:
                return {
                    i: format for i, format in enumerate(output_formats, start=1)
                }.get(choice, 'all')


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Use the script directory as the input folder for video files
input_folder = script_dir

# Ensure the output folder exists
output_folder = os.path.join(script_dir, 'output_folder')

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the video file extensions you want to search for (both lowercase and uppercase)
video_extensions = ('.3gp', '.3GP', '.asf', '.ASF', '.avi', '.AVI', '.flv', '.mkv', '.MKV', '.mov', '.MOV', '.mp4', '.MP4', '.mpeg', '.MPEG', '.mpg', '.MPG', '.mxf', '.MXF', '.ts', '.TS', '.webm', '.WEBM', '.wmv', '.WMV')

# Find video files
video_files = find_video_files(input_folder, video_extensions)

# Create a set of existing output file names for quick lookup
existing_output_files = set(os.listdir(output_folder))

# Allow the user to select a file for conversion or a folder for VIDEO_TS or AVCHD
print("Select a file or folder for conversion:")
for i, item in enumerate(video_files, start=1):
    print(f"{i}. {item}")
video_ts_folders = find_video_ts_folders(input_folder)
avchd_folders = find_avchd_folders(input_folder)
for i, folder in enumerate(video_ts_folders, start=len(video_files) + 1):
    parent_directory = os.path.dirname(folder)  # Get the full path to the parent directory
    print(f"{i}. VIDEO_TS folder: {parent_directory}")
for i, folder in enumerate(avchd_folders, start=len(video_files) + 1 + len(video_ts_folders)):
    print(f"{i}. AVCHD folder: {folder}")

selected_index = input("Enter the number of the file or folder to convert: ")

#####################################################################


try:
    selected_index = int(selected_index) - 1
    if 0 <= selected_index < len(video_files):
        selected_item = video_files[selected_index]

        # Get the relative path of the item from the script directory
        relative_path = os.path.relpath(selected_item, script_dir).replace(os.path.sep, '-')
        output_format = get_output_format()

        if output_format == 'all':
            # Convert to all available formats
            for output_ext in ['.webm', '.avi', '.mkv', '.mov', '.ts', '.3gp', '.mxf', '.asf', '.flv', '.mp4', '.mpeg', '.mpg', '.wmv']:
                output_file = os.path.join(output_folder, f'{os.path.splitext(relative_path)[0]}{output_ext}')
                if os.path.basename(output_file) in existing_output_files:
                    user_choice = handle_overwrite_prompt(output_file)
                    if user_choice == 'o':
                        if output_ext == '.webm':
                            subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libvpx-vp9', '-b:v', '2M', '-c:a', 'libvorbis', output_file])
                        elif output_ext == '.mxf':
                            subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'pcm_s16le', '-strict', 'experimental', '-ar', '48000', output_file])
                        elif output_ext == '.mpeg' or output_ext == '.mpg':
                            subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'mpeg2video', '-b:v', '5M', '-c:a', 'mp2', '-ar', '44100', output_file])
                        else:
                            subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', '-ar', '48000', output_file])
                        print(f"Conversion of {selected_item} to {output_ext} complete. Saved as {output_file}")
                    else:
                        print(f"Skipping conversion of {selected_item} to {output_ext}.")
                else:
                    if output_ext == '.webm':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libvpx-vp9', '-b:v', '2M', '-c:a', 'libvorbis', output_file])
                    elif output_ext == '.mxf':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'pcm_s16le', '-strict', 'experimental', '-ar', '48000', output_file])
                    elif output_ext == '.mpeg' or output_ext == '.mpg':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'mpeg2video', '-b:v', '5M', '-c:a', 'mp2', '-ar', '44100', output_file])
                    else:
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', '-ar', '48000', output_file])
                    print(f"Conversion of {selected_item} to {output_ext} complete. Saved as {output_file}")
        else:
            output_file = os.path.join(output_folder, f'{os.path.splitext(relative_path)[0]}{output_format}')

            # Check if the output file already exists in the output_folder
            if os.path.basename(output_file) in existing_output_files:
                user_choice = handle_overwrite_prompt(output_file)
                if user_choice == 'o':
                    if output_format == '.webm':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libvpx-vp9', '-b:v', '2M', '-c:a', 'libvorbis', output_file])
                    elif output_format == '.mxf':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'pcm_s16le', '-strict', 'experimental', '-ar', '48000', output_file])
                    elif output_format == '.mpeg' or output_format == '.mpg':
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'mpeg2video', '-b:v', '5M', '-c:a', 'mp2', '-ar', '44100', output_file])
                    else:
                        subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', '-ar', '48000', output_file])
                    print(f"Conversion of {selected_item} to {output_format} complete. Saved as {output_file}")
                else:
                    print(f"Skipping conversion of {selected_item} to {output_format}.")
            else:
                if output_format == '.webm':
                    subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libvpx-vp9', '-b:v', '2M', '-c:a', 'libvorbis', output_file])
                elif output_format == '.mxf':
                    subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'pcm_s16le', '-strict', 'experimental', '-ar', '48000', output_file])
                elif output_format == '.mpeg' or output_format == '.mpg':
                    subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'mpeg2video', '-b:v', '5M', '-c:a', 'mp2', '-ar', '44100', output_file])
                else:
                    subprocess.run(['ffmpeg', '-y', '-i', selected_item, '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', '-ar', '48000', output_file])
                print(f"Conversion of {selected_item} to {output_format} complete. Saved as {output_file}")


                
                
#####################################################################
    elif len(video_files) <= selected_index < len(video_files) + len(video_ts_folders):
        # User selected a VIDEO_TS folder
        selected_index -= len(video_files)
        selected_folder = video_ts_folders[selected_index]

        # Use the parent directory name as the output file name
        parent_directory = os.path.basename(os.path.dirname(selected_folder))
        output_format = get_output_format()

        if output_format == 'all':
            # Convert to all available formats
            for output_ext in ['.webm', '.avi', '.mkv', '.mov', '.ts', '.3gp', '.mxf', '.asf', '.flv', '.mp4', '.mpeg', '.mpg', '.vob', '.wmv']:
                output_file = os.path.join(output_folder, f'{parent_directory}{output_ext}')
                if os.path.basename(output_file) in existing_output_files:
                    user_choice = handle_overwrite_prompt(output_file)
                    if user_choice == 'o':
                        vob_files = [os.path.join(selected_folder, file) for file in os.listdir(selected_folder) if file.endswith('.VOB')]
                        vob_files.sort()
                        subprocess.run(['ffmpeg', '-y', '-i', f'concat:{"|".join(vob_files)}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                        print(f"Conversion of {parent_directory} to {output_ext} complete. Saved as {output_file}")
                    else:
                        print(f"Skipping conversion of {parent_directory} to {output_ext}.")
                else:
                    vob_files = [os.path.join(selected_folder, file) for file in os.listdir(selected_folder) if file.endswith('.VOB')]
                    vob_files.sort()
                    subprocess.run(['ffmpeg', '-y', '-i', f'concat:{"|".join(vob_files)}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                    print(f"Conversion of {parent_directory} to {output_ext} complete. Saved as {output_file}")
        else:
            output_file = os.path.join(output_folder, f'{parent_directory}{output_format}')

            # Check if the output file already exists in the output_folder
            if os.path.basename(output_file) in existing_output_files:
                user_choice = handle_overwrite_prompt(output_file)
                if user_choice == 'o':
                    vob_files = [os.path.join(selected_folder, file) for file in os.listdir(selected_folder) if file.endswith('.VOB')]
                    vob_files.sort()
                    subprocess.run(['ffmpeg', '-y', '-i', f'concat:{"|".join(vob_files)}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                    print(f"Conversion of {parent_directory} to {output_format} complete. Saved as {output_file}")
                else:
                    print(f"Skipping conversion of {parent_directory} to {output_format}.")
            else:
                vob_files = [os.path.join(selected_folder, file) for file in os.listdir(selected_folder) if file.endswith('.VOB')]
                vob_files.sort()
                subprocess.run(['ffmpeg', '-y', '-i', f'concat:{"|".join(vob_files)}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                print(f"Conversion of {parent_directory} to {output_format} complete. Saved as {output_file}")



#####################################################################
    elif len(video_files) + len(video_ts_folders) <= selected_index:
        # User selected an AVCHD folder
        selected_index -= len(video_files) + len(video_ts_folders)
        selected_folder = avchd_folders[selected_index]

        # Use the parent directory name as the output file name
        parent_directory = os.path.basename(selected_folder)
        output_format = get_output_format()

        if output_format == '.webm':
            output_file = os.path.join(output_folder, f'{os.path.splitext(relative_path)[0]}.webm')

        # Check if the output format is WebM
        if output_format == '.webm':
            output_file = os.path.join(output_folder, f'{os.path.splitext(relative_path)[0]}.webm')

        if output_format == 'all':
            # Convert to all available formats
            combined_output_file = os.path.join(output_folder, f'{parent_directory}.webm')
            if os.path.basename(combined_output_file) in existing_output_files:
                user_choice = handle_overwrite_prompt(combined_output_file)
                if user_choice == 'o':
                    combined_input_files = []
                    stream_folder = os.path.join(selected_folder, 'BDMV', 'STREAM')
                    mts_files = [f for f in os.listdir(stream_folder) if f.lower().endswith('.mts')]
                    for mts_file in mts_files:
                        input_file = os.path.join(stream_folder, mts_file)
                        combined_input_files.append(input_file)

                    # Use ffmpeg to combine the .mts files into a single output file
                    input_files = '|'.join(combined_input_files)
                    subprocess.run(['ffmpeg', '-y', '-i', f'concat:{input_files}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', combined_output_file])
                    print(f"Conversion of {len(mts_files)} .mts files to WebM complete. Saved as {combined_output_file}")
                else:
                    print(f"Skipping conversion of {parent_directory} to WebM.")
            else:
                combined_input_files = []
                stream_folder = os.path.join(selected_folder, 'BDMV', 'STREAM')
                mts_files = [f for f in os.listdir(stream_folder) if f.lower().endswith('.mts')]
                for mts_file in mts_files:
                    input_file = os.path.join(stream_folder, mts_file)
                    combined_input_files.append(input_file)

                # Use ffmpeg to combine the .mts files into a single output file
                input_files = '|'.join(combined_input_files)
                subprocess.run(['ffmpeg', '-y', '-i', f'concat:{input_files}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', combined_output_file])
                print(f"Conversion of {len(mts_files)} .mts files to WebM complete. Saved as {combined_output_file}")
        else:
            output_file = os.path.join(output_folder, f'{parent_directory}{output_format}')

            # Check if the output file already exists in the output_folder
            if os.path.basename(output_file) in existing_output_files:
                user_choice = handle_overwrite_prompt(output_file)
                if user_choice == 'o':
                    stream_folder = os.path.join(selected_folder, 'BDMV', 'STREAM')
                    mts_files = [f for f in os.listdir(stream_folder) if f.lower().endswith('.mts')]
                    combined_input_files = []
                    for mts_file in mts_files:
                        input_file = os.path.join(stream_folder, mts_file)
                        combined_input_files.append(input_file)

                    # Use ffmpeg to combine the .mts files into a single output file
                    input_files = '|'.join(combined_input_files)
                    subprocess.run(['ffmpeg', '-y', '-i', f'concat:{input_files}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                    print(f"Conversion of {len(mts_files)} .mts files to {output_format} complete. Saved as {output_file}")
                else:
                    print(f"Skipping conversion of {parent_directory} to {output_format}.")
            else:
                stream_folder = os.path.join(selected_folder, 'BDMV', 'STREAM')
                mts_files = [f for f in os.listdir(stream_folder) if f.lower().endswith('.mts')]
                combined_input_files = []
                for mts_file in mts_files:
                    input_file = os.path.join(stream_folder, mts_file)
                    combined_input_files.append(input_file)

                # Use ffmpeg to combine the .mts files into a single output file
                input_files = '|'.join(combined_input_files)
                subprocess.run(['ffmpeg', '-y', '-i', f'concat:{input_files}', '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-c:a', 'aac', '-strict', 'experimental', output_file])
                print(f"Conversion of {len(mts_files)} .mts files to {output_format} complete. Saved as {output_file}")


    else:
        print("Invalid selection.")
except ValueError:
    print("Invalid input.")

print("Conversion complete.")
