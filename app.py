import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

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
            return redirect(url_for('display_image',
                                    filename=filename))
        else:
            flash('Invalid image type')
            return redirect(request.url)
    #return '''
    #<!doctype html>
    #<title>Upload new File</title>
    #<h1>Art Style Identifier</h1>
    #<p> Upload your image! (accepts .png, .jpg, .jpeg) </p>
    #<form method=post enctype=multipart/form-data>
      #<input type=file name=file>
      #<input type=submit value=Upload>
    #</form>
    #'''
#from flask import send_from_directory

#@app.route('/uploads/<filename>')
#def uploaded_file(filename):
    #return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)