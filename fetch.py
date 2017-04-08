import sys
from random import random
import requests
import pymongo

BB_TL = (59.8946, 29.8735)
BB_BR = (59.8657, 29.9534)

mongo = pymongo.MongoClient('mongodb://localhost:27017')['qr_instagram']


def random_coord():
    def randrange(start, end):
        return start + random() * (end - start)

    lat = randrange(BB_BR[0], BB_TL[0])
    lon = randrange(BB_BR[1], BB_TL[1])
    return lat, lon

    
def locations(lat, lng):
	url = 'https://api.instagram.com/v1/locations/search?lat={lat}&lng={lng}&access_token={at}'.format(
		lat=lat,
		lng=lng,
		at=access_token
	)
	res = requests.get(url)
	data = res.json()
	try:
		locations = data['data']
		return locations
	except:
		print(data)
		return None


access_token = sys.argv[1]
for i in range(1000):
	lat, lon = random_coord()
	ls = locations(lat, lon)
	if not ls:
		break
	print(i, len(ls))
	for loc in ls:
		mongo.locations.update({'id': loc['id']}, loc, upsert=True)
