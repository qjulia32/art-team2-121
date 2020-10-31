import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from fastai.basic_train import load_learner
from fastai.vision import open_image
#from flask_cors import CORS,cross_origin
# need to google how to install pytorch

app = Flask(__name__)

#path to user uploads
UPLOAD_FOLDER = 'static/uploads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"


#back end model, outputs prediction of given image 
learn = load_learner(path='./models', file='trained_model.pkl')
classes = learn.data.classes

def predict_single(img_file):
    'function to take image and return prediction'
    prediction = learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    #probs = {category: round(float(probs_list[8]))}
    return category
        #'category': classes[prediction[1].item()],
        #'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)}
    

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

# for uploading an image
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
        if file and not allowed_file(file.filename):
            flash('Error: Invalid image type')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            classification = predict_single(full_path)
            return render_template("upload.html", user_image = full_path, classify = classification, scroll = "display")
