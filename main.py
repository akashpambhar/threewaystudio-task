import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
import magic
from mutagen import File

UPLOAD_FOLDER = './uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def determine_file_type(filename):
    mime = magic.Magic()
    file_type = mime.from_file(filename)
    return file_type

@app.route("/", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        if 'file' not in request.files:
            print("no file part")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if file:
            file.save(file_path)
            print(os.stat(path=file_path))
            print(filename)
            al = File(file_path).info.length
            print(al)

        if "Audio" not in determine_file_type(file_path):
                os.remove(file_path)
                print('Not an audio file')
                return redirect(request.url)
        return "uploaded"

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)