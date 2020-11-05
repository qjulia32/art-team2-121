import os
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
#from fastai.basic_train import load_learner
#from fastai.vision import open_image

app = Flask(__name__)
app.secret_key = "secret key"


#
#learn = load_learner(path='./models', file='trained_model.pkl')
#classes = learn.data.classes

def predict_single(img_file):
    'function to take image and return prediction'
    prediction = learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    print("Prediction: %s" % category)
    return category
    

@app.route('/')
def upload_form():
	return render_template('upload.html')


# for uploading an image
# NEEDS WORK: this function and classifications doesn't work for new updated upload and display that works on heroku
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.file)
        if file and not allowed_file(file.filename):
            return redirect(request.file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            classification = predict_single(full_path)
            return render_template("upload.html", classify = classification)
