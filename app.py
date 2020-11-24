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


#main page
@app.route("/")
def upload():
    return render_template("upload.html")

#more info page
@app.route("/about")
def about():
    return render_template("about.html")

# check if correct extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# upload and classify image
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """On failure, return the current template with an error message
       On success, return a new template with appropriate classifications"""
    if request.method == 'POST':
        file = request.files["image"]
        if file.filename == '':
            return render_template("upload.html", message = "Please upload an image first (see step 1)", scroll = "display")
        elif file and not allowed_file(file.filename):
            return render_template("upload.html", message = "Unsupported file extension: please upload a .jpg/.jpeg", scroll = "display")
        else:
            # convert pillow image to fastai recognizable image
            img_pil = PIL.Image.open(file)
            if img_pil.size[0] > img_pil.size[1] > 6000000: 
              return render_template("upload.html", message = "Image too large, please upload an image with dimensions of less than 2560 x 2560 pixels", scroll = "display")
            else:
              img_tensor = T.ToTensor()(img_pil)
              image = Image(img_tensor)
              match = ['Top match: ', 'Second match: ', 'Third match: '] # match text with proper result
              if 'style' in request.form and 'artist' not in request.form and 'time' not in request.form:
                  style = predict(image, "style")[0]
                  styleprob = predict(image, "style")[1] 
                  return render_template("classifications.html", style = style, styleprob = styleprob, match = match)
              elif 'artist' in request.form and 'style' not in request.form and 'time' not in request.form:
                  artist  = predict(image, "artist")[0]
                  artistprob = predict(image, "artist")[1]
                  return render_template("classifications.html", artist= artist, artistprob = artistprob, match = match)
              elif 'time' in request.form and 'artist' not in request.form and 'style' not in request.form:
                  firststyle = predict(image, "style")[0][0]
                  period = style_to_time(firststyle)
                  return render_template("classifications.html", period = period, match = match)
              elif 'style' in request.form and 'artist' in request.form and 'time' not in request.form:
                  style = predict(image, "style")[0]
                  styleprob = predict(image, "style")[1]                
                  artist  = predict(image, "artist")[0]
                  artistprob = predict(image, "artist")[1]
                  return render_template("classifications.html", style = style, styleprob = styleprob, artist= artist, artistprob = artistprob, match = match)
              elif 'style' in request.form and 'time' in request.form and 'artist' not in request.form:
                  style = predict(image, "style")[0]
                  styleprob = predict(image, "style")[1]                
                  firststyle = style[0]
                  period = style_to_time(firststyle)
                  return render_template("classifications.html", style = style, styleprob = styleprob, period = period, match = match)
              elif 'artist' in request.form and 'time' in request.form and 'style' not in request.form:
                  firststyle = predict(image, "style")[0][0] 
                  period = style_to_time(firststyle)
                  artist  = predict(image, "artist")[0]
                  artistprob = predict(image, "artist")[1]
                  return render_template("classifications.html", artist = artist, artistprob = artistprob, period = period, match = match)
              elif 'artist' and 'time' and 'style' in request.form:
                  style = predict(image, "style")[0]
                  styleprob = predict(image, "style")[1]                
                  artist = predict(image, "artist")[0]
                  artistprob = predict(image, "artist")[1]
                  firststyle = style[0]
                  period = style_to_time(firststyle)
                  return render_template("classifications.html", style = style, styleprob = styleprob, artist = artist, artistprob = artistprob, period = period, match = match)
              else: 
                  return render_template("upload.html", message = "Please choose a classifier after uploading (see step 2)", scroll = "display")


#predict style or artist on uploaded image
def predict(img_file, classifier):
    """Arguments: fastai recognizable image, string describing which classifier(s) were checked
    Returns: prediction of the top three matches for either style or artist, depending on the 
    classifier checked"""
    if classifier == 'style':
        pathname = 'style.pkl'
    else: 
        pathname = 'artist-stage-6.pkl'
    style = load_learner(path='./models', file=pathname)
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
    probs = round(max(probs_list) * 100, 2)
    probs2 = round(probs_list[secondi] * 100, 2)
    probs3 = round(probs_list[thirdi] * 100, 2)
    #Return top 2 matches and percentage
    return [category, category2, category3], [probs, probs2, probs3]

#find time period based on style
def style_to_time(prediction):
  if prediction == "Abstract":
    return "1950s-present"
  elif prediction == "Academicism":
    return "1560-1900"
  elif prediction == "American Realism":
    return "1850s-1900s"
  elif prediction == "Art Brut":
    return"1940s"
  elif prediction == "Art Deco":
    return "1908-1935"
  elif prediction == "Classicism":
    return "1400s-1600s"
  elif prediction == "Abstract Expressionism" or prediction == "Magic Realism" or prediction == "Color Field Painting" or prediction == "Tachisme":
    return "1940s-1950s"
  elif prediction == "Conceptual Art" or prediction == "Op Art" or prediction == "Contemporary Realism":
    return"1960s-1970s"
  elif prediction == "Concretism" or prediction == "Pop Art":
    return "1950s-1970s"
  elif prediction == "New Realism" or prediction == "Minimalism" or prediction == "Hard Edge Painting":
    return "1950s-1960s"
  elif prediction == "Cloisonnism":
    return "1880s"
  elif prediction == "Dada":
    return "1916-1924"
  elif prediction == "Divisionism":
    return "1884-1904"
  elif prediction == "Fauvism":
    return "1904-1910"
  elif prediction == "Futurism":
    return "1909-1914"
  elif prediction == "Ink and wash painting":
    return "618-907"
  elif prediction == "Luminism":
    return "1850s-1970s"
  elif prediction == "Lyrical Abstraction":
    return "1945-1960"
  elif prediction == "Metaphysical art":
    return "1911-1920"
  elif prediction == "Naturalism":
    return "1865-1900"
  elif prediction == "Neo-Expressionism":
    return "1970s-1980s"
  elif prediction == "Neo-Romanticism":
    return "1930-1955"
  elif prediction == "Neoplasticism":
    return "1917-1931"
  elif prediction == "Orientalism":
    return "1700s-1800s"
  elif prediction == "Pointillism":
    return "1880s-1890s"
  elif prediction == "Post-Painterly Abstraction":
    return "1955-1965"
  elif prediction == "Precisionism":
    return "1920s-1930s"
  elif prediction == "Proto Renaissance":
    return "1300s-1400s"
  elif prediction == "Regionalism":
    return "1925-1945"
  elif prediction == "Shin-haga":
    return "1910-1960"
  elif prediction == "Social Realism":
    return "1930-1945"
  elif prediction == "Sosaku hanga":
    return "1600s-1800s"
  elif prediction == "Synthetic Cubism":
    return "1912-1914"
  elif prediction == "Tenebrism":
    return "1600s"
  elif prediction == "Art Informel":
    return "1943-1950s"
  elif prediction == "Art Nouveau (Modern)":
    return "1890-1910"
  elif prediction == "Baroque":
    return "1600-1700s"
  elif prediction == "Cubism":
    return "1908-1912"
  elif prediction == "Early Renaissance":
    return "1280-1400"
  elif prediction == "Expressionism":
    return "1905-1920"
  elif prediction == "High Renaissance":
    return "1490s-1527"
  elif prediction == "Impressionism":
    return "1867-1886"
  elif prediction == "Mannerism (Late Renaissance)":
    return "1520s-1590s"
  elif prediction == "Naïve Art (Primitivism)":
    return "1300s-1400s"
  elif prediction == "Neoclassicism":
    return "1760s-1850s"
  elif prediction == "Northern Renaissance":
    return "1430-1580"
  elif prediction == "Post-Impressionism":
    return "1886-1905"
  elif prediction == "Realism":
    return "1830s-1880s"
  elif prediction == "Rococo":
    return "1740s-1770s"
  elif prediction == "Romanticism":
    return "1800-1850"
  elif prediction == "Surrealism":
    return "1924-1966"
  elif prediction == "Symbolism":
    return "1886-1900"
  elif prediction == "Ukiyo-e":
    return "1615-1868"
  else:
    return "An error has occurred. Please try again."
