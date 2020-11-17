"""This script runs an app that will determine the style,
time period, or artist associated with the input image."""

from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from PIL import Image
from fastai.basic_train import load_learner
from fastai.vision import *
import torchvision.transforms as T

app = Flask(__name__)
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
#app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024


@app.route("/")
@app.route("/upload")
@app.route("/upload.html")
def upload():
    return redirect("/static/upload.html")

@app.route("/")
@app.route("/about")
@app.route("/about.html")
def about():
    return redirect("/static/about.html")

# check if correct extension
def allowed_file(filename):
    """This function determines if the file is the correct extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload and classify image
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """This function is used to upload and classify the input image."""
    if request.method == 'POST':
        file = request.files["image"]
        if file and not allowed_file(file.filename):
            return "not available for this extension. Please upload a .jpg/.jpeg"
        else:
            #following doesn't work with onsubmit return in html
            #if 'style' in request.form:
                #call style or artist function
            print(request.form)
            # convert pillow image to fastai recognizable image
            img_pil = PIL.Image.open(file)
            img_tensor = T.ToTensor()(img_pil)
            image = Image(img_tensor)
            classify = predict_style(image)
            print(classify)
            return "</br> Top match: {} ({}%) </br> Second match: {} ({}%) </br> Third match: {} ({}%)".format(classify[0], classify[1], classify[2], classify[3], classify[4], classify[5])


def predict_style(img_file):
    'function to take image and return prediction'
    style = load_learner(path='./models', file='style_25_100.pkl')
    classes = style.data.classes #list of possible art periods
    prediction = style.predict(img_file)
    array = np.array(prediction)
    probs_list = array[2].numpy()
    #find second largest
    secondmax = 0
    thirdmax = 0
    for i in range(len(probs_list)):
        if probs_list[i]>secondmax and probs_list[i] != max(probs_list):
            secondmax = probs_list[i]
            secondi = i
        if probs_list[i] > thirdmax and probs_list[i] != secondmax and probs_list[i] != max(probs_list):
            thirdmax = probs_list[i]
            thirdi = i
    category = classes[prediction[1].item()]
    category2 = classes[secondi]
    category3 = classes[thirdi]
    probs = str(round(max(probs_list) * 100, 2))
    probs2 = str(round(probs_list[secondi] * 100, 2))
    probs3 = str(round(probs_list[thirdi] * 100, 2))
    #Return top 2 matches and percentage
    return category, probs, category2, probs2, category3, probs3


    
def predict_artist(img_file):
    'function to take image and return prediction'
    artist = load_learner(path='./models', file='artist.pkl')
    classes = artist.data.classes
    prediction = artist.predict(img_file)
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    #NEEDSWORK: print top 3 matches and percentages
    return category
