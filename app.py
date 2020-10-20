import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
# following modules don't work, fastai not able to be installed locally
#from fastai import *
#from fastai.basic_train import load_learner
#from fastai.vision import * #open_image
#from flask_cors import CORS,cross_origin
# need to pip install torch (google for window)
#import cloudinary as Cloud
#from cloudinary.uploader import upload
#from cloudinary.utils import cloudinary_url

#path to user uploads
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

# code to upload image
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            return render_template("upload.html", user_image = full_path)
        else:
            flash('Invalid image type')
            return redirect(request.url)

