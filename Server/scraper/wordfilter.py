import nltk
import string
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re
import pandas as pd
import time

from searchscraper import scrape_google

#Creating tools for filtering
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
lemmatize = WordNetLemmatizer().lemmatize
stop_words = set(stopwords.words('english'))

#Take title, description, content of search results and outputs them as a dictionary per site.
def filter_words_from_search(search_results):
    t0 = time.time()
    if (len(search_results) > 0):
        site_list = []
        for page_num in range(len(search_results)):
            page = search_results[page_num]
            tokens = tokenizer.tokenize(page['title'] + " " + page['description'] + " " + page['content'])
            filteredwords = [x for x in [w for w in tokens] if (x not in string.punctuation and not x.isdigit())]
            lemmatized_words = [lemmatize(w.lower()) for w in filteredwords if (lemmatize(w.lower()) not in stop_words and w != "")]
            site_list.append(Text(lemmatized_words))
        dict_list = [dict(site.vocab()) for site in site_list]
        site_dict = {}
        for page_num in range(len(search_results)):
            site_dict[search_results[page_num]['link']] = dict_list[page_num]
        t1 = time.time()
        print("Filter Time: " + str(t1 - t0))
        return site_dict
    else:
        return {'error': 404}

#Compiles search and filter into one command
def scraper(querystring):
	results = scrape_google(querystring, 50, 'en')

	return filter_words_from_search(results)

#Outputs as a Panda DataFrame
def scraper_df(querystring):
    results = pd.DataFrame.from_dict(scraper(querystring), orient="index").fillna(0)
    #results.columns = ['Site' if x=='index' else x for x in results.columns]
    return results

if __name__ == "__main__":
    print(scraper("+"))
