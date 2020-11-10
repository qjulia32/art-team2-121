# includes functions and model name for artist
# mostly copied from predict_single in app.py in Catherine's branch

# back end model, outputs prediction of given image
artist_model = 'artist-stage-3.pkl' # 61.3% accuracy and classifies 53 artists
artist_learn = load_learner(path='./models', file=artist_model)
artist_classes = artist_learn.data.classes

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
    prediction = artist_learn.predict(open_image(img_file))
    probs_list = prediction[2].numpy()
    return {
        'category': artist_classes[prediction[1].item()],
        'probs': {c: round(float(probs_list[i]), 5) for (i, c) in enumerate(artist_classes)}
    }