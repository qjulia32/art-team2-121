import numpy as np
import pandas as pd
import os, os.path, zipfile, shutil

PIC_NUMBER = 50

# Goal: find styles with 50+ images and put them in their respective folders
# assumptions: train_1 data and train_info.csv already downloaded/unzipped

# NOTE: basically, train_info.csv has info on ALL training images, but we only
# downloaded train_1, so the csv has info on files we don't have. I made a work
# around in order to get 50 images, as you'll see below

# NOTE: this creates a data folder w/ 36/133 total styles w/ 1,800 total pictures

# csv_path = "INSERT THE PATH TO THE train_info.csv FILE HERE INCLUDING NAME train_info.csv"
csv_path = "C:/Users/qjuli/Downloads/train_info.csv/train_info.csv"

pbn = pd.read_csv(csv_path)
pbn = pbn.fillna(np.nan)
pbn.drop(labels = ["title","genre","date","artist"], axis=1, inplace=True)
pbn = pbn.dropna(how='any',axis=0)

stylesNumDict = {}

for index, row in pbn.iterrows():
    if row["style"] in stylesNumDict:
        stylesNumDict[row["style"]] += [row["filename"]]
    else:
        stylesNumDict[row["style"]] = [row["filename"]]


# path =  "PATH TO UNZIPPED TRAIN_1 Data and end w/ backslash -> /"
path =  "C:/Users/qjuli/Downloads/train_1/train_1/"

styleCount = {}

for style in stylesNumDict.keys():

    styleCount[style] = []

    for image in stylesNumDict[style]:
        img_old_path = path+image
        if os.path.exists(img_old_path):
            styleCount[style].append(image)

for style, count in styleCount.items():

    if len(count) >= PIC_NUMBER:
        # print("working on", style)

        # folder_path = "INSERT DIRECTORY OF YOUR CLONED GIT REPO HERE, IN A different DATA FOLDER OF SOME SORT and end w/ backslash -> /"+style
        folder_path = "C:/Users/qjuli/Downloads/Harvey Mudd/Fall 2020/software_dev/art-team2-121/small_"+str(PIC_NUMBER)+"_data/"+style

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # print(style, count[:PIC_NUMBER])
        for image in count[:PIC_NUMBER]:
            img_old_path = path+image
            img_new_path = folder_path+ "/"+image
            shutil.copy(img_old_path, img_new_path)

            # print("  adding image", img_old_path)
            if not os.path.exists(img_old_path):
                print("    something went wrong rip")
            # # can also move it if you want to store space
            # # shutil.move(img_old_path, img_new_path)

