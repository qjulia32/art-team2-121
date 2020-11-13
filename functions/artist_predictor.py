"""This script contains functions and the model for the artist. Similar to predict_single in app.py."""
# includes functions and model name for artist
# mostly copied from predict_single in app.py in Catherine's branch

# back end model, outputs prediction of given image
ARTIST_MODEL = 'artist-stage-3.pkl' # 61.3% accuracy and classifies 53 artists
ARTIST_LEARN = load_learner(path='./models', file=ARTIST_MODEL)
ARTIST_CLASSES = ARTIST_LEARN.data.classes

# possible idea 1: pass in the learner
# predict_single('img_file.jpg', artist_learn, artist_classes)
def predict_single(img_file, learn, classes):
    'function to take image and return prediction'
    prediction = learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        'category': classes[prediction[1].item()],
        'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(classes)}
    }

# possible idea 2: have a separate function for artist
def artist_predict_single(img_file):
    'function to take image and return prediction'
    prediction = ARTIST_LEARN.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        'category': ARTIST_CLASSES[prediction[1].item()],
        'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(ARTIST_CLASSES)}
    }
