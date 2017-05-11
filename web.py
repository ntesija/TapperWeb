import threading
from flask import Flask, jsonify, render_template, url_for, abort, request
from pymongo import MongoClient
from updateDatabase import updateLoop

app = Flask(__name__)

client = MongoClient()
db = client['heroku_qst864ll']

@app.route("/")
def home():
	locationCollection = db['locations']
	tappedLocations = locationCollection.find()
	mainList = locationCollection.find()
	return render_template("main.html", tappedLocations=tappedLocations, mainList=mainList)

@app.route("/list/<location>")
def list(location):
	notSorted = True
	collection = db[location]
	locationCollection = db['locations']
	tappedLocations = locationCollection.find()

	if collection.count() == 0:
		abort(404)
	data = collection.find()
	typeList = []
	types=[]
	if 'sort' in request.args:
		if request.args.get('sort') == 'type':
			data = sorted(data, key=lambda beer: beer['currentType'])
			count = 1
			for beer in data:
				if beer['currentType'] not in typeList:
					typeList.append(beer['currentType'])
					types.append([beer['currentType'], count])
				count += 1
			notSorted = False
	return render_template("beer-list.html", beerList=data, location=location, tappedLocations=tappedLocations, notSorted=notSorted, types=types)

@app.errorhandler(404)
def pageNotFound(e):
	locationCollection = db['locations']
	tappedLocations = locationCollection.find()
	return render_template("404.html", tappedLocations=tappedLocations), 404

@app.errorhandler(500)
def internalError(e):
	locationCollection = db['locations']
	tappedLocations = locationCollection.find()
	return render_template("500.html", tappedLocations=tappedLocations), 500


if __name__ == "__main__":
	app.run(threaded=True, debug=True)