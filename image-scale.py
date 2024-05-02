from PIL import Image
import os

def resize_and_compress_image(file_path, output_dir, max_size=1080, quality=85):
    """
    Resizes and compresses an image to fit within a max_size box, reduces its file size for web use, and saves it to the output directory.
    - file_path: Path to the original image file.
    - output_dir: Directory where the modified image will be saved.
    - max_size: Maximum width or height of the resized image.
    - quality: Quality of the output image (1-100) for JPEG files. Higher means better quality and larger file size.
    """
    img = Image.open(file_path)
    # Resize the image
    img.thumbnail((max_size, max_size), Image.ANTIALIAS)
    
    # Define output path
    output_path = os.path.join(output_dir, os.path.basename(file_path))
    
    # Save the file
    if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
        img.save(output_path, 'JPEG', optimize=True, quality=quality)
    elif file_path.lower().endswith('.png'):
        img.save(output_path, 'PNG', optimize=True)

def main():
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir('.'):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f'Processing {file}...')
            resize_and_compress_image(file, output_dir)
            print(f'{file} processed.')

if __name__ == "__main__":
    main()
