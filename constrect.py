import os
import shutil
import json
from fuzzywuzzy import fuzz

# Load configurations from reference.json
with open('reference.json', 'r') as file:
    configurations = json.load(file)

# List of configurations with keywords and destination folders
for config in configurations:
    print(f"Keywords: {config['keywords']}, Destination: {config['destination']}")

# Base directory where the script is stored
base_directory = os.path.dirname(os.path.abspath(__file__))
# Directory where videos are stored, within the same directory as the script
source_directory = os.path.join(base_directory, "video")

def move_video(video_path, destination_folder):
    """Move the video to the destination folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created folder: {destination_folder}")
    
    try:
        shutil.move(video_path, destination_folder)
        print(f"Moved '{video_path}' to '{destination_folder}'")
    except Exception as e:
        print(f"Error moving '{video_path}': {e}")

def match_video_to_config(video_name):
    """Match a video name to a configuration using fuzzy matching."""
    for config in configurations:
        for keyword in config["keywords"]:
            # Fuzzy matching score threshold
            if fuzz.partial_ratio(video_name.lower(), keyword.lower()) > 80:
                return config["destination"]
    return None

def organize_videos():
    """Organize videos by moving them to respective folders based on fuzzy matching."""
    try:
        for file_name in os.listdir(source_directory):
            file_path = os.path.join(source_directory, file_name)
            
            # Check if it's a file (ignores directories)
            if os.path.isfile(file_path):
                destination_folder = match_video_to_config(file_name)
                if destination_folder:
                    move_video(file_path, destination_folder)
                else:
                    print(f"No match found for '{file_name}', skipping.")
    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    organize_videos()
