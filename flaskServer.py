from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the folder path where you want to save the superchat files
superchat_folder = 'path/to/save/superchats/as/txts/'  # IMPORTANT <<< REPLACE

@app.route('/save-superchat', methods=['POST'])
def save_superchat():
    try:
        superchat_data = request.json
        sender_name = superchat_data['senderName']
        superchat_message = superchat_data['superchatMessage']
        
        # Generate a unique filename (e.g., using a counter or timestamp)
        filename = f"superchat_{len(os.listdir(superchat_folder)) + 1}.txt"
        
        # Write sender's name and superchat message to a new text file in the specified folder
        with open(os.path.join(superchat_folder, filename), 'w') as file:
            file.write(f"Sender: {sender_name}\n")
            file.write(f"Message: {superchat_message}\n")
        return jsonify({'message': 'Superchat saved successfully', 'filename': filename})
    
    except Exception as e:
        return jsonify({'error': 'Failed to process request', 'details': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
