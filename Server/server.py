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
from wordfilter import scraper, scraper_df

# Import tfidf
from tfidf import tfidf

# Routes
@app.route("/")
def root():
	return "YOU SHALL NOT PASS!"

@app.route("/scrape")
def scrape():
	return jsonify(tfidf(scraper(request.args.get("querystring"))))

# Running the server
if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000)