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
from wordfilter import scraper, scraper_df, scrape_urls

# Import tfidf
from tfidf import tfidf
from tfidf_df import tfidf_df

# Import url sorter
from url_sorter import sort_urls

# Routes
@app.route("/")
def root():
	return "YOU SHALL NOT PASS!"

@app.route("/scrape")
def scrape():
	scraper_values = scraper_df(request.args.get("querystring"), 1000)
	tfidf_values = tfidf(scraper_values)
	tfidf_pd_values = tfidf_df(scraper_values, request.args.get("querystring"))
	return jsonify({
		"tfidf" : tfidf_values,
		"specifics" : tfidf_pd_values
	})

# Running the server
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)