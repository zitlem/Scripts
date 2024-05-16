import os
import re

# Dictionary mapping Russian characters to their English phonetic equivalents
russian_to_english = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh', 'З': 'Z',
    'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
}

def convert_to_english(text):
    # Convert each word in the text from Russian to English phonetic equivalent
    english_text = ' '.join(''.join(russian_to_english.get(char, char) for char in word) for word in re.findall(r'\b\w+\b', text))
    
    return english_text

def rename_files_and_folders(directory):
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        for name in files:
            # Rename files
            old_path = os.path.join(root, name)
            new_filename = convert_to_english(os.path.splitext(name)[0]) + os.path.splitext(name)[1]
            new_path = os.path.join(root, new_filename)
            os.rename(old_path, new_path)
            print(f"Renamed file '{old_path}' to '{new_path}'")
        
        for name in dirs:
            # Rename directories
            old_path = os.path.join(root, name)
            new_name = convert_to_english(name)
            new_path = os.path.join(root, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed directory '{old_path}' to '{new_path}'")

# Get the current directory
current_directory = os.getcwd()

# Rename files and folders in the current directory

rename_files_and_folders(current_directory)