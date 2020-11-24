import json
import random

# a python wrapper for the Github API (pip install PyGithub)
# https://pygithub.readthedocs.io/en/latest/index.html
from github import Github

# id for art-team2-121 repo:
ID = 298410561

g = Github()
repo = g.get_repo(ID)

def get_similar(classifier, num_images):
    ''' 
        FOR STYLE
        Displays random images of a certain style or artist from our Github repo
        This function assumes that images are organized based on the classifier
        classifer: the predicted category (style or artist) 
                    (does not have to be a string! Can come straight from predictor)
        num_images: The number of images to get'''

    contents = repo.get_contents("data/" + str(classifier))

    sim_images = []     # paths of chosen images

    while len(sim_images) < num_images:
        img_name = random.choice(contents).path
        if img_name not in sim_images:
            sim_images.append(img_name)
    
    style = [] # array of json objs
    for i in range(len(sim_images)):
        style.append(repo.get_contents(sim_images[i]).download_url)
        
    
    return style

def get_similar_artist(classifier, num_images):
    '''
        artist version of get_similar 
    '''
    contents = repo.get_contents("data/artist" + str(classifier))

    sim_images = []     # paths of chosen images

    while len(sim_images) < num_images:
        img_name = random.choice(contents).path
        if img_name not in sim_images:
            sim_images.append(img_name)

    artist = [] # array of json objs
    for i in range(len(sim_images)):
        artist.append(repo.get_contents(sim_images[i]).download_url)
    
    return artist

# print(get_similar("Zen", 3))
