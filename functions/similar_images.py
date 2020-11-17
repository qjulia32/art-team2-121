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
    ''' Displays random images of a certain style or artist from our Github repo
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

    return sim_images

    # TODO: Save/display images
    # Access the image with repo.get_contents(img_name)
    # Will return a JSON with the format described here (content is a file):
    # https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#contents

# get_similar("Zen", 3)
