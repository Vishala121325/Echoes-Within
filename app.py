
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import zipfile
from flask import send_file
import json
from datetime import datetime
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['CAPSULE_FILE'] = 'capsules.json'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # Max 100MB

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_capsules():
    # Check if the capsule file exists
    if os.path.exists(app.config['CAPSULE_FILE']):
        with open(app.config['CAPSULE_FILE'], 'r') as f:
            return json.load(f)
    return []  # Return an empty list if the file doesn't exist
# Define a custom filter to format datetime objects

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, datetime):
        return value.strftime(format)
    return value

def load_capsule_by_id(capsule_id):
    # Load all the capsules from the JSON file
    capsules = load_capsules()
    
    # Find the capsule with the matching ID
    capsule = next((c for c in capsules if c['id'] == float(capsule_id)), None)
    
    return capsule


def save_capsules(capsules):
    with open(app.config['CAPSULE_FILE'], 'w') as f:
        json.dump(capsules, f, default=str)

@app.route('/')
def home():
    capsules = load_capsules()
    now = datetime.now().isoformat()
    return render_template('index.html', capsules=capsules, now=now)


@app.route('/download_all/<capsule_id>', methods=['GET'])
def download_all(capsule_id):
    # Load the capsule data (modify according to your implementation)
    capsule = load_capsule_by_id(capsule_id)  # Replace with your method to get a capsule by ID

    if not capsule:
        return "Capsule not found", 404

    # Get the media files (photos, videos, audios)
    files = []

    # Add photos if they exist
    photos = capsule.get('photos', [])
    for photo in photos:
        files.append(os.path.join(app.config['UPLOAD_FOLDER'], photo))

    # Add videos if they exist
    videos = capsule.get('videos', [])
    for video in videos:
        files.append(os.path.join(app.config['UPLOAD_FOLDER'], video))

    # Add audio clips if they exist
    audios = capsule.get('audios', [])
    for audio in audios:
        files.append(os.path.join(app.config['UPLOAD_FOLDER'], audio))

    # Create a ZIP file in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file in files:
            if os.path.exists(file):
                zip_file.write(file, os.path.basename(file))  # Add each file to the zip
            else:
                print(f"File {file} not found")

    zip_buffer.seek(0)  # Rewind to the beginning of the file

    # Return the zip file as a downloadable file
    return send_file(zip_buffer, as_attachment=True, download_name="capsule_files.zip", mimetype="application/zip")

@app.route('/add')
def add_capsule():
    return render_template('add.html')

@app.route('/save_capsule', methods=['POST'])
def save_capsule():
    message = request.form.get('message')
    unlock_date = request.form.get('unlockDate')
    name = request.form.get('name')  # Capture the name from the form

    # Get the list of photos, videos, and audio files
    photos = request.files.getlist('photos[]')
    videos = request.files.getlist('videos[]')
    audios = request.files.getlist('audios[]')  # New: Getting audio files

    photo_filenames = []
    video_filenames = []
    audio_filenames = []  # New: List for storing audio filenames

    # Save photos
    for photo in photos:
        if photo and photo.mimetype.startswith('image/'):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo_filenames.append(filename)

    # Save videos
    for video in videos:
        if video and video.mimetype.startswith('video/'):
            filename = secure_filename(video.filename)
            video.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            video_filenames.append(filename)

    # Save audio files
    for audio in audios:
        if audio and audio.mimetype.startswith('audio/'):
            filename = secure_filename(audio.filename)
            audio.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            audio_filenames.append(filename)  # Add audio filenames to list

    # Load existing capsules and append the new one
    capsules = load_capsules()
    capsules.append({
        'id': datetime.now().timestamp(),
        'name': name,  # Save the capsule name
        'message': message,
        'photos': photo_filenames,
        'videos': video_filenames,
        'audios': audio_filenames,  # New: Adding audio filenames
        'unlockDate': unlock_date
    })

    save_capsules(capsules)

    return redirect(url_for('home'))

@app.route('/get_capsules')
def get_capsules():
    capsules = load_capsules()
    return jsonify(capsules)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<float:capsule_id>', methods=['POST'])
def delete_capsule(capsule_id):
    capsules = load_capsules()
    capsule = next((c for c in capsules if c['id'] == capsule_id), None)
    if capsule:
        # Delete associated files
        for photo in capsule.get('photos', []):
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        for video in capsule.get('videos', []):
            video_path = os.path.join(app.config['UPLOAD_FOLDER'], video)
            if os.path.exists(video_path):
                os.remove(video_path)

        # Remove capsule from list
        capsules = [c for c in capsules if c['id'] != capsule_id]
        save_capsules(capsules)
        return redirect(url_for('home'))
    else:
        return "Capsule not found", 404
    
@app.route('/open/<capsule_id>')
def open_capsule(capsule_id):
    capsules = load_capsules()
    capsule = next((c for c in capsules if str(c['id']) == str(capsule_id)), None)
    if not capsule:
        return "Capsule not found!", 404
    return render_template('open.html', capsule=capsule)

if __name__ == '__main__':
    app.run(debug=True)
