from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from PIL import Image
from fastai.basic_train import load_learner
from fastai.vision import *
import torchvision.transforms as T

app = Flask(__name__)
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
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
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload and classify image
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files["image"]
        if file and not allowed_file(file.filename):
            return "not available for this extension. Please upload a .jpg, .jpeg or .png"
        else:
            print(request.form)
            # convert pillow image to fastai recognizable image
            img_pil = PIL.Image.open(file)
            img_tensor = T.ToTensor()(img_pil)
            image = Image(img_tensor)
            return predict_style(image)


def predict_style(img_file):
    'function to take image and return prediction'
    style = load_learner(path='./models', file='style_25_100.pkl')
    classes = style.data.classes
    prediction = style.predict(img_file)
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    #NEEDSWORK: print top 3 matches and percentages
    return category

    
def predict_artist(img_file):
    'function to take image and return prediction'
    artist = load_learner(path='./models', file='artist.pkl')
    classes = artist.data.classes
    prediction = artist.predict(img_file)
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    #NEEDSWORK: print top 3 matches and percentages
    return category
