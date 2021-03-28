#!flask/bin/python
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from reader import read_pan_card

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'PNG','JPEG','JPG'}

app = Flask(__name__,template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

@app.route('/')
def index():
    return render_template('pan_card_uploader.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/extract_data', methods=['POST'])
def extract_pan_card_data():
    try:
        if request.method == 'POST':
            # check if there is a file in the request
            if 'pan_card_file' not in request.files:
                return render_template('pan_card_uploader.html', msg='No file selected')
            file_data = request.files.get('pan_card_file')
            # if no file is selected
            if file_data.filename == '':
                return render_template('pan_card_uploader.html', msg='No file selected')

            # check if the file has been uploaded
            if file_data.filename and allowed_file(file_data.filename):
                data = {}
                file_name = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file_data.filename))
                file_data.save(file_name)
                data = read_pan_card(file_name)
                return render_template('pan_card_details.html',data=data)
            return render_template('pan_card_uploader.html', msg="Please upload a valid file with extension png/jpg/jpeg!")
        return render_template('pan_card_uploader.html',msg="Invalid Request")
    except Exception as ex:
        raise ex


if __name__ == '__main__':
    app.run(debug=True)
