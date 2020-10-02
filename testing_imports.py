import numpy as np
import pandas as pd
import os

# for dirname, _, filenames in os.walk(my_path):
#     print(dirname)
#     break

#     for filename in filenames:
#         os.path.join(dirname, filename)

# # returns file path from the train.zip
# def imgPath(num):
#     path = "C:/Users/qjuli/Downloads/train_1/train_1" + num
#     return path

# # prints out image from filename column
# def printImg(num):
#     path = imgPath(num)
#     print(path)
#     plt.figure(figsize=(12,12))
#     plt.subplot(1,2,1)
#     img = cv2.imread(path)
#     imgplot = plt.imshow(img)

#     plt.show()


# import train info along with removing art without any style

csv_path = "C:/Users/qjuli/Downloads/train_info.csv/train_info.csv"
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

# print(stylesNumDict)

import os, os.path, shutil
path =  "C:/Users/qjuli/Downloads/train_1/train_1/"
for style in stylesNumDict.keys():
    folder_path = "C:/Users/qjuli/Downloads/Harvey Mudd/Fall 2020/software_dev/art-team2-121/data/"+style

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    for image in stylesNumDict[style]:

        img_old_path = path+image
        if os.path.exists(img_old_path):
            img_new_path = folder_path+ "/"+image
            shutil.copy(img_old_path, img_new_path)