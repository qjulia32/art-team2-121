# Api access key:	 	ec4718eeefd44297
# Api secret key:	 	b0b9f15a93b6f064

# Well this program will take forever because of the API limitations. It saves the dictionary after entering each painting, so if
# the connection is interrupted by host, our current progress will be saved

import requests
import os
import time
import json
from datetime import datetime, timedelta

# The API has a maximum of 10 requests per 2.5 seconds, and 400 requests per hour. count will track how many we've made and 
# we can wait until the time limit has passed once it has reached its maximum
count = 3
DELAY_TIME = 1
one_hour = datetime.now() + timedelta(hours=1)      # One hour from current time

session = requests.Session()
key = session.post("https://www.wikiart.org/en/Api/2/login?accessCode=ec4718eeefd44297&secretCode=b0b9f15a93b6f064")
key = key.json()["SessionKey"]

# Dictionary of all paintings. key = style, value = list of painting ids
# Also includes an entry with the total number of paintings
paintings = {}
paintings["numPaintings"] = 0

response = session.get("https://www.wikiart.org/en/api/2/MostViewedPaintings?authSessionKey" + key)

# Must convert to json dictionary to be able to access element by key
response = response.json()

# Iterates through pages of results
while response["hasMore"]:
    next = response["paginationToken"]

    for p in response["data"]:
        id = p["id"]
        p = session.get("https://www.wikiart.org/en/api/2/Painting?id="+ id + "&authSessionKey=" + key)
        p = p.json()
        count += 1

        # Enter painting ID into the dictionaries under its styles
        for style in p["styles"]:
            if not (style in paintings):
                paintings[style] = [id]
            else:
                paintings[style].append(id)

        paintings["numPaintings"] += 1

        # Sleeps if reached maximum requests
        if count % 9 == 0:
            time.sleep(DELAY_TIME)
        if count % 399 == 0:
            while one_hour > datetime.now():
                time.sleep(DELAY_TIME)
            one_hour = datetime.now() + timedelta(hours=1)

        # Writes current paintings dictionary to style_dict.txt
        # Formats as json so we can easily load it later
        f = open("style_dict.txt", "w")
        json.dump(paintings, f)
        f.close()
    
    # Moves to next page
    response = session.get("https://www.wikiart.org/en/api/2/MostViewedPaintings?paginationToken=" + next + "&authSessionKey=" + key)
    response = response.json()
    count += 1

# How to download image to file for future reference:
#
#
# "image" is a link to the isolated image
# image = session.get(response["image"])
# file = open("img.jpg", "wb")
# file.write(image.content)
# file.close()

