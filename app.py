from flask import Flask, request, send_file, jsonify
import os
import tempfile
from format_chords import process_lines

app = Flask(__name__)

# Assuming your script is a function that processes lyrics with chords
# Let's assume it returns the path to the processed file
def process_lyrics_with_chords(lyrics_with_chords):
    # Replace this with the actual logic of your script
    # For now, we'll just save the lyrics to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', newline='\n', encoding='utf-8') as temp_file:
        process_lines(lyrics_with_chords.replace('[', '').replace(']', '').splitlines(), temp_file)
        temp_file.close()
        return temp_file.name

@app.route('/process-lyrics', methods=['POST'])
def process_lyrics():
    data = request.get_json()
    if not data or 'lyrics' not in data:
        return jsonify({'error': 'No lyrics provided'}), 400
    
    lyrics_with_chords = data['lyrics']
    
    # Process the lyrics with your script
    processed_file_path = process_lyrics_with_chords(lyrics_with_chords)

    # Send the processed file to the user for download
    return send_file(processed_file_path, as_attachment=True, download_name='baked_lyrics.txt')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")