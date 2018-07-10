import nltk
import string
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd

from searchscraper import scrape_google

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
lemmatize = WordNetLemmatizer().lemmatize
stop_words = set(stopwords.words('english'))

def filter_words_from_search(search_results):
    if (len(search_results) > 0):
        site_list = []
        for page_num in range(len(search_results)):
            page = search_results[page_num]
            tokens = tokenizer.tokenize(page['title'] + " " + page['description'] + " " + page['content'])
            filteredwords = [x for x in [w for w in tokens] if (x not in string.punctuation and not x.isdigit())]
            lemmatized_words = [lemmatize(w.lower()) for w in filteredwords if (lemmatize(w.lower()) not in stop_words and w != "")]
            site_list.append(Text(lemmatized_words))
        dict_list = [dict(site.vocab()) for site in site_list]
        return dict_list
    else:
        return {'error': 500}

def scraper(querystring):
	results = scrape_google(querystring, 10, 'en')

	return filter_words_from_search(results)

def scraper_df(querystring):
    return pd.DataFrame(scraper(querystring)).fillna(0)

# if __name__ == "__main__":
#   print(scraper("sgcodecampus.com"))

#print(scraper("lolxd"))
