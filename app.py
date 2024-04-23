from flask import Flask, render_template, request, send_file
import os
import zipfile
import tempfile

app = Flask(__name__)

# Directory for storing uploaded files
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Directory for storing compressed files
COMPRESSED_FOLDER = os.path.join(tempfile.gettempdir(), 'compressed')
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

# Create upload and compressed directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COMPRESSED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress():
    files = request.files.getlist('files[]')

    if len(files) == 0:
        return 'No files selected'

    # List to store paths of uploaded files
    uploaded_file_paths = []

    for file in files:
        if file.filename == '':
            continue

        # Save uploaded file to temporary directory
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(uploaded_file_path)
        uploaded_file_paths.append(uploaded_file_path)

    # Compress files into a single ZIP file
    compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], 'compressed_files.zip')
    with zipfile.ZipFile(compressed_file_path, 'w') as zipf:
        for uploaded_file_path in uploaded_file_paths:
            zipf.write(uploaded_file_path, os.path.basename(uploaded_file_path))

    # Delete uploaded files from server
    for uploaded_file_path in uploaded_file_paths:
        os.remove(uploaded_file_path)

    return send_file(compressed_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
