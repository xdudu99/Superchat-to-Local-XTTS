import os
import time
from datetime import datetime
import requests
from langdetect import detect_langs, DetectorFactory
import pygame

# Initialize Pygame mixer
pygame.mixer.init()

# Folder where the superchat text files are saved
superchat_folder = 'path/to/superchats/txts/' #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IMPORTANT

# Folder where WAV files are saved
output_folder = 'path/where/wavs/will/be/stored'#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IMPORTANT

# Maximum number of superchat text files to keep
max_superchat_files = 20  # Adjust this number as needed

# Set langdetect DetectorFactory seed for consistent results
DetectorFactory.seed = 0

# Function to read the latest superchat message from a text file
def read_latest_superchat(file_path):
    try:
        # Read the content of the file
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            lines = file.readlines()
            
            # Look for the line starting with "Message:"
            for line in lines:
                if line.startswith('Message:'):
                    # Extract the message after "Message:"
                    superchat_message = line.split('Message:')[1].strip()
                    return superchat_message
            
            # If no "Message:" line is found, return None
            print(f'No "Message:" line found in file: {file_path}')
            return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

# Function to detect language of the superchat message
def detect_language(superchat_message):
    try:
        # Detect the language of the text (ensure text is UTF-8 encoded)
        result = detect_langs(superchat_message)
        detected_lang = result[0].lang
        confidence = result[0].prob
        return detected_lang, confidence
    except Exception as e:
        print(f"Error detecting language: {e}")
        return None, 0.0

# Function to format and send a POST request with superchat data
def send_superchat_data(superchat_message, file_path):
    if superchat_message is None:
        return
    
    # Example: Detect language of the superchat message
    detected_lang, confidence = detect_language(superchat_message)
    
    # Example: Constructing the POST body
    data = {
        'text': superchat_message,
        'speaker_wav': 'speaker.wav',  # Replace with actual speaker WAV file or identifier <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< IMPORTANT
        'language': detected_lang if detected_lang else 'en',  # Default to 'en' if language detection fails
        'file_name_or_path': f'superchat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav' # Example file name
    }
    
    # Example: Sending POST request
    url = 'http://localhost:8020/tts_to_file'
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print(f'Superchat data from {os.path.basename(file_path)} sent successfully.')
        
        # Delete the file after sending POST request
        os.remove(file_path)
        print(f'Deleted file: {file_path}')
        
        # Play the audio file after successful POST request
        play_last_audio(output_folder)  # Replace with your actual audio file path
        
    except requests.exceptions.RequestException as e:
        print(f'Error sending superchat data: {e}')

def play_last_audio(folder):
    try:
        # Get a list of all WAV files in the folder
        wav_files = [f for f in os.listdir(folder) if f.endswith('.wav')]
        
        # Sort the files by creation time (most recent first)
        wav_files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
        
        if wav_files:
            # Get the path to the most recent WAV file
            latest_wav_file = os.path.join(folder, wav_files[0])
            
            # Play the audio file using Pygame mixer
            pygame.mixer.music.load(latest_wav_file)
            pygame.mixer.music.play()
            
            # Wait until playback finishes
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)  # Adjust the tick rate as needed
        
        else:
            print(f'No WAV files found in {folder}')
    
    except pygame.error as e:
        print(f'Error playing audio: {e}')

# Function to monitor for new files in the directory
def monitor_superchat_files():
    while True:
        # Get the list of text files in the folder
        files = os.listdir(superchat_folder)
        
        if files:
            for file_name in files:
                file_path = os.path.join(superchat_folder, file_name)
                superchat_message = read_latest_superchat(file_path)
                if superchat_message:
                    send_superchat_data(superchat_message, file_path)
        
        # Check the number of files and delete old files if necessary
        current_files = os.listdir(superchat_folder)
        num_files = len(current_files)
        
        if num_files > max_superchat_files:
            # Sort files by modification time (oldest first)
            files_to_delete = sorted(current_files, key=lambda x: os.path.getmtime(os.path.join(superchat_folder, x)))
            
            # Delete the oldest files until the count is within limit
            for file_to_delete in files_to_delete[:num_files - max_superchat_files]:
                os.remove(os.path.join(superchat_folder, file_to_delete))
                print(f'Deleted file: {file_to_delete}')
        
        # Sleep for some time before checking again (e.g., every 5 seconds)
        time.sleep(5)

# Main function to start monitoring
def main():
    monitor_superchat_files()

if __name__ == '__main__':
    main()
