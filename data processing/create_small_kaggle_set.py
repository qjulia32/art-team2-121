import numpy as np
import pandas as pd
import os, os.path, zipfile, shutil


# min number of images per style for style to be included
PIC_NUMBER = 50 # pics you want per style that passes the threshold

# TODO: change these
THRESHOLD = 50

# TODO: choose your category
categories = ["artist", "title", "style", "date", "genre"]
category = "style"

# Goal: find category with THRESHOLD+ images and put PIC_NUMBER of them in their respective folders
# assumptions: train_1.zip, train_info.csv, and all_data_info.csv already downloaded/unzipped

# NOTE: basically, train_info.csv has info on ALL training images, but we only
# downloaded train_1, so the csv has info on files we don't have. I made a work
# around in order to get 50 images, as you'll see below
# NOTE: with THRESHOLD = 50 and PIC_Number = 50: there's 36/133 total styles w/ 1,800 total pictures

# NOTE: all_data_info.csv has actual artist names (it's hased in the train_info.csv b/c the whole point is to guess it)
# so, we will cross reference our given pictures by the category title and whether it's in train_1.csv
# download it here: https://www.kaggle.com/c/painter-by-numbers/data?select=all_data_info.csv

# train_csv_path = "INSERT THE PATH TO THE train_info.csv FILE HERE INCLUDING NAME train_info.csv"
train_csv_path = "C:/Users/qjuli/Downloads/train_info.csv/train_info.csv"

# data_csv_path = "INSERT THE PATH TO THE all_data_info.csv FILE HERE"
data_csv_path = "C:/Users/qjuli/Downloads/all_data_info.csv"


train_pbn = pd.read_csv(train_csv_path)
train_pbn = train_pbn.fillna(np.nan)
# print(train_pbn.head())
labels = [l for l in categories if l != category]
# print(labels)
train_pbn.drop(labels=labels, axis=1, inplace=True)
train_pbn = train_pbn.dropna(how='any',axis=0)
# print(train_pbn.head())

if category == "artist":
    # train_pbn has hashed artist names, don't know hash function whoops
    train_pbn = train_pbn.rename(columns={"artist": "hash_artist"})

    # it's database joining time: join on filename, replace artist from train with artist from data
    data_pbn = pd.read_csv(data_csv_path)
    data_pbn = data_pbn.fillna(np.nan)
    data_pbn = data_pbn.rename(columns={"new_filename": "filename"})
    # df.join(other.set_index('key'), on='key')
    train_pbn = train_pbn.join(data_pbn.set_index('filename'), on='filename')
    # print(train_pbn.head())

catNumDict = {}

for index, row in train_pbn.iterrows():
    if row[category] in catNumDict:
        catNumDict[row[category]] += [row["filename"]]
    else:
        catNumDict[row[category]] = [row["filename"]]


# path =  "PATH TO UNZIPPED TRAIN_1 Data and end w/ backslash -> /"
path =  "C:/Users/qjuli/Downloads/train_1/train_1/"

catCount = {}

for cat in catNumDict.keys():

    catCount[cat] = []

    for image in catNumDict[cat]:
        img_old_path = path+image
        if os.path.exists(img_old_path):
            catCount[cat].append(image)

folder = 0
for cat, count in catCount.items():

    # remove extra leading/trailing spaces so folder names aren't weird
    cat = cat.strip()

    if len(count) >= THRESHOLD:

        folder += 1
        print("working on", cat)

        # folder_path = "INSERT DIRECTORY OF YOUR CLONED GIT REPO HERE, IN A different DATA FOLDER OF SOME SORT and end w/ backslash -> /"+style
        folder_path = "C:/Users/qjuli/Downloads/Harvey Mudd/Fall 2020/software_dev/data/small_"+str(PIC_NUMBER)+"_"+str(THRESHOLD)+"_"+category+"_data/"+cat
        print(folder_path)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # print(cat, count[:PIC_NUMBER])
        for image in count[:PIC_NUMBER]:
            img_old_path = path+image
            img_new_path = folder_path+"/"+image
            shutil.copy(img_old_path, img_new_path)

            # print("  adding image", img_old_path)
            if not os.path.exists(img_old_path):
                print("    something went wrong rip")
            # # can also move it if you want to save space
            # # shutil.move(img_old_path, img_new_path)

print("number of", category, ":", folder)