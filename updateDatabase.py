from globals import locations
from tapperWeb import getTapperData
from bottleOpenerWeb import getBottleOpenerData
from pymongo import MongoClient
import sys, time, datetime, pymongo

client = MongoClient()
db = client['heroku_qst864ll']

updateTime = 86400.0 # 1 Day

def updateDatabase():
	output = ""
	for location in locations:
		try:
			beerList = getTapperData(location)
			try:
				bottleList = getBottleOpenerData(location)
				data = beerList + bottleList
			except:
				print("Error getting bottle data for {}\n".format(location))
				data = beerList
			data = sorted(data, key=lambda beer: beer['ppv'], reverse=True)
			collection = db[location]
			collection.delete_many({})
			collection.insert_many(data)

			locationCollection = db['locations']
			tappedLocation = locationCollection.find_one({'city': location})
			if not tappedLocation:
				locationCollection.insert({'city': location})
		except TypeError as e:
			print(e)
		except:
			print("Error getting Tapper data for {}: {}\n".format(location, sys.exc_info()[0]))
			tappedLocation = locationCollection.find_one({'city': location})
			if tappedLocation:
				locationCollection.remove({'city': location})
				
def updateLoop():
	startTime = time.time()
	while True:
		updateDatabase()
		time.sleep(updateTime - ((time.time() - startTime) % 60.0))


if __name__ == "__main__":
	updateLoop()