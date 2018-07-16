from gevent import monkey
monkey.patch_all()

# Generic Imports
from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Start up flask with CORS
app = Flask(__name__)
CORS(app)

# Import scraper
sys.path.append(os.path.abspath("./scraper"))
from wordfilter import scraper, scraper_df, scrape_urls, get_related_words

# Import tfidf
from tfidf import tfidf
from tfidf_df import tfidf_df

# Import url sorter
from url_sorter import sort_urls

# Import tinydb
from tinydb import TinyDB, Query
db = TinyDB("db.json")

# Index global variable
indexStorage = {}

# Routes
@app.route("/")
def root():
	return "This is the JvJ SERVER!"

@app.route("/scrape")
def scrape():
	try:
		querystring = request.args.get("querystring")
		print("Recieved scrape query: " + querystring)
		scraper_values, stuff, index = scraper_df(querystring, 50)
		tfidf_values = tfidf(scraper_values)
		tfidf_pd_values = tfidf_df(scraper_values, stuff, querystring)
		db.insert({"querystring" : querystring, "tfidf" : tfidf_values, "tfidf_pd_values" : tfidf_pd_values})
		indexStorage[querystring] = index
		return jsonify({
			"tfidf" : tfidf_values,
			"specifics" : tfidf_pd_values
		})
	except Exception as e:
		print(e)
		queryer = Query()
		if len(db.search(queryer.querystring == querystring)):
			return jsonify({
					"tfidf" : db.search(queryer.querystring == querystring)[0]["tfidf"],
					"specifics" : db.search(queryer.querystring == querystring)[0]["tfidf_pd_values"]
				})
		else:
			return jsonify({
					"tfidf" : "ERROR",
					"specifics" : "ERROR"
				})
	print(scraper_values)

@app.route("/relatedWords")	
def relatedWords():
	try:
		print("Recieved relatedWords query!")
		print("Querystring: " + request.args.get("querystring"))
		print("Word: " + request.args.get("wordSearch"))
		queryer = Query()
		if len(indexStorage[request.args.get("querystring")]):
			return jsonify(get_related_words(request.args.get("wordSearch"), indexStorage[request.args.get("querystring")]))
	except Exception as e:
		print(e)
		return "Error"

# Running the server
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)
