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
    """Redirect to where they should go"""
    return redirect("/static/upload.html")


# for uploading an image
# NEEDS WORK: this function and classifications doesn't work for new updated upload and display that works on heroku

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files["image"]
        """
        if file.filename == '':
            return redirect(request.file)
        if file and not allowed_file(file.filename):
            return render_template("upload.html", wrongext = 1, scroll = "display")
        if file:"""
        img_pil = PIL.Image.open(file)
        img_tensor = T.ToTensor()(img_pil)
        image = Image(img_tensor)
        classify = predict_single(image)
        return predict_single(image)

learn = load_learner(path='./models', file='trained_model.pkl')
classes = learn.data.classes

def predict_single(img_file):
    'function to take image and return prediction'
    prediction = learn.predict(img_file)
    probs_list = prediction[2].numpy()
    category = classes[prediction[1].item()]
    print("Prediction: %s" % category)
    return category