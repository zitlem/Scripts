import os
import rawpy
import imageio

def convert_raw_to_jpeg(raw_image_path, output_path):
    with rawpy.imread(raw_image_path) as raw:
        rgb = raw.postprocess()
    imageio.imsave(output_path, rgb)

def convert_all_raw_images_in_directory(directory_path):
    raw_extensions = {'.cr2', '.nef', '.dng', '.arw'}  # Add or remove extensions as needed
    
    for filename in os.listdir(directory_path):
        if os.path.splitext(filename)[1].lower() in raw_extensions:
            raw_image_path = os.path.join(directory_path, filename)
            output_path = os.path.join(directory_path, os.path.splitext(filename)[0] + '.jpg')
            convert_raw_to_jpeg(raw_image_path, output_path)
            print(f"Converted {filename} to JPEG.")

# Use the directory of the script as the directory to search for raw images
script_directory = os.path.dirname(os.path.abspath(__file__))
convert_all_raw_images_in_directory(script_directory)
