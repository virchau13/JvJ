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
from wordfilter import scrape


@app.route("/")
def root():
	return "YOU SHALL NOT PASS!"

@app.route("/scrape")
def scraper():
	return scrape("sgcodecampus.com")

if __name__ == "__main__":
	app.run()