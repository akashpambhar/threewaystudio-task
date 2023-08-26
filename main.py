import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import magic
from mutagen import File
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from datetime import date

UPLOAD_FOLDER = 'static'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:akash@localhost:3306/threewaystudio'

db = SQLAlchemy(app)

class AudioFile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Float, nullable=False)
    upload_date = db.Column(db.Date)
    extension = db.Column(db.String(50))
    duration = db.Column(db.Float, nullable=False)
    path = db.Column(db.String(300), nullable=False)

    def __init__(self, name, size, upload_date, extension, duration, path):
        self.name = name
        self.size = size
        self.upload_date = upload_date
        self.extension = extension
        self.duration = duration
        self.path = path


def determine_file_type(filename):
    mime = magic.Magic()
    file_type = mime.from_file(filename)
    return file_type

@app.route("/", methods=["POST", "GET"])
def upload():
    db.create_all()
    res = ""
    duration_exceeds = False

    if request.method == "POST":
        files = request.files.getlist('file[]')
        file_count = 0
        for file in files:
            res = handle_upload(file)
            if(res == -1):
                duration_exceeds = True
                break
            file_count += res
        
        res = f'{file_count} uploaded of {len(files)}'

    audio_files = AudioFile.query.all()
    return render_template("index.html", audio_files=audio_files, duration_exceeds=duration_exceeds, file_count=res)


@app.route('/delete_audio/<int:id>', methods=['POST'])
def delete_audio(id):
    audio_file = AudioFile.query.get(id)
    if audio_file:
        os.remove(audio_file.path)
        db.session.delete(audio_file)
        db.session.commit()
    return redirect("/")

def handle_upload(file):
    if not file:
        return 0
    if file.filename == '':
        print('No selected file')
        return 0

    filename = secure_filename(file.filename)
    file_path = os.path.join(
        app.root_path, app.config['UPLOAD_FOLDER'], filename)
    
    file.save(file_path)

    if not check_if_audio:
        return 0

    duration = round(File(file_path).info.length/60, 2)
    if not check_duration(file_path, duration):
        return -1

    extension = ""
    if len(filename.rsplit('.', 1)) > 2:
        extension = filename.rsplit('.', 1)[1]

    save_to_database(filename, file_path, extension, duration)
    
    return 1

def check_if_audio(file_path):
    if "Audio" not in determine_file_type(file_path):
        os.remove(file_path)
        print('Not an audio file')
        return False
    
    return True

def check_duration(file_path, duration):
    total_duration = db.session.query(
        func.sum(AudioFile.duration)).scalar()
    total_duration = total_duration if total_duration else 0

    if duration + total_duration > 10:
        os.remove(file_path)
        print("duration exceeds")
        return False
    
    return True

def save_to_database(filename, file_path, extension, duration):
    audio_file = AudioFile(
        filename,
        round(bytes_to_megabytes(os.stat(path=file_path).st_size), 2),
        date.today(),
        extension,
        duration,
        file_path
    )

    
    db.session.add(audio_file)
    db.session.commit()

def bytes_to_megabytes(bytes_size):
    return bytes_size / (1024 ** 2)

if __name__ == "__main__":
    app.run(debug=True)