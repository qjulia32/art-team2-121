import numpy as np
import pandas as pd
import os, os.path, zipfile, shutil

# first install numpy and pandas on your computer

# download training_1.zip from this website:
# https://www.kaggle.com/c/painter-by-numbers/data?select=train_1.zip

# unzip the training_1 data, might take like 10 min
train_1_path = "INSERT PATH TO train_1.zip HERE INCLUDING THE NAME train_1.zip"
with zipfile.ZipFile(train_1_path, 'r') as zip_ref:
    zip_ref.extractall(train_1_path)

# then download train_info.csv from this website:
# https://www.kaggle.com/c/painter-by-numbers/data?select=train_info.csv
# unzip this one too, can copy code from above or do it manually, takes like a second

# import train info along with removing art without any style
csv_path = "INSERT THE PATH TO THE train_info.csv FILE HERE INCLUDING NAME train_info.csv"
pbn = pd.read_csv(csv_path)
pbn = pbn.fillna(np.nan)
pbn.drop(labels = ["title","genre","date","artist"], axis=1, inplace=True)
pbn = pbn.dropna(how='any',axis=0)

# Goal: basically put all the images of the same style into a folder

stylesNumDict = {}

for index, row in pbn.iterrows():
    if row["style"] in stylesNumDict:
        stylesNumDict[row["style"]] += [row["filename"]]
    else:
        stylesNumDict[row["style"]] = [row["filename"]]


path =  "PATH TO UNZIPPED TRAIN_1 Data and end w/ backslash -> /"
for style in stylesNumDict.keys():
    folder_path = "INSERT DIRECTORY OF YOUR CLONED GIT REPO HERE IN A DATA FOLDER OF SOME SORT and end w/ backslash -> /"+style

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image in stylesNumDict[style]:

        img_old_path = path+image
        if os.path.exists(img_old_path):
            img_new_path = folder_path+ "/"+image
            shutil.copy(img_old_path, img_new_path)
            # can also move it if you want to store space
            # shutil.move(img_old_path, img_new_path)
