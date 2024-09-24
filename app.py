from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
import json
from model import probe_model_5l_profit

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'data_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['data_file']
        # If the user does not select a file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Process the file
            with open(filepath, 'r') as f:
                data = json.load(f)
            result = probe_model_5l_profit(data["data"])
            # Save result to session or pass it via URL
            return render_template('results.html', result=result)
    return render_template('upload.html')

@app.route('/results')
def results():
    # This route is handled in the upload_file function
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
