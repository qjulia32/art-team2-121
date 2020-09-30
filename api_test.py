# Api access key:	 	ec4718eeefd44297
# Api secret key:	 	b0b9f15a93b6f064

import requests

session = requests.Session()
session.get("https://www.wikiart.org/en/Api/2/login?accessCode=ec4718eeefd44297&secretCode=b0b9f15a93b6f064")

response = session.get("https://www.wikiart.org/en/api/2/Painting?id=57727089edc2cb3880be55d5")
response = response.json()
style = response["styles"]

print(response["styles"])

image = session.get(response["image"])
file = open("img.jpg", "wb")
file.write(image.content)
file.close()

# 'id': '57727089edc2cb3880be55d5', 'title': 'Don Quixote and Sancho Setting Out', 'url': 'don-quixote-and-sancho-setting-out-1863', 'artistUrl': 'gustave-dore', 'artistName': 'Gustave Dore', 'artistId': '57726d81edc2cb3880b48481', 'completitionYear': 1863, 'width': 466, 'image': 'https://uploads5.wikiart.org/images/gustave-dore/don-quixote-and-sancho-setting-out-1863.jpg!Large.jpg', 'height': 600