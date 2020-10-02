# Api access key:	 	ec4718eeefd44297
# Api secret key:	 	b0b9f15a93b6f064

# PROGRESS:
# I figured out how to access and save images from WikiArt. It looks like the only way we can access every painting in one request is
# to access a list sorted by popularity. Additionally, this only returns the short version of painting information, so we have to make an 
# additional request with each painting ID to get the style. We can also request image dimensions, so hopefully we won't have to resize.

import requests
import os
import time

DELAY_TIME = 0.00001

session = requests.Session()
key = session.post("https://www.wikiart.org/en/Api/2/login?accessCode=ec4718eeefd44297&secretCode=b0b9f15a93b6f064")
key = key.json()["SessionKey"]

# Dictionary of all paintings. key = style, value = list of painting ids
paintings = {}

response = session.get("https://www.wikiart.org/en/api/2/MostViewedPaintings?authSessionKey" + key)

# Must convert to json dictionary to be able to access element by key
response = response.json()

# while response["hasMore"]:
for p in response["data"]:
    id = p["id"]
    # print(id)
    p = session.get("https://www.wikiart.org/en/api/2/Painting?id="+ id + "&authSessionKey" + key)
    p = p.json()
    for style in p["styles"]:
        if not (style in paintings):
            paintings[style] = [id]
        else:
            paintings[style].append(id)
    time.sleep(DELAY_TIME)

print(paintings)

# style = response["styles"]

# print(response["styles"])

# "image" is a link to the isolated image
# image = session.get(response["image"])
# file = open("img.jpg", "wb")
# file.write(image.content)
# file.close()

