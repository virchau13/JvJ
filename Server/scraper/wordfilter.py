import nltk
import string
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import re

from searchscraper import scrape_google

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
regex = re.compile('[^a-zA-Z]')

def filter_words_from_search(search_results):
    site_list = []
    if (len(search_results) > 0):
        for page_num in range(len(search_results)):
            filteredwords = []
            page = search_results[page_num]
            tokens = tokenizer.tokenize(page['title'] + " " + page['description'] + " " + page['content'])
            filteredwords += [x for x in [w for w in tokens] if (x not in string.punctuation and not x.isdigit())]
            lemmatized_words = []
            for word in filteredwords:
                word = lemmatizer.lemmatize(regex.sub('', word).lower())
                if word not in stop_words and word != "":
                    lemmatized_words.append(word)

            site_list.append(Text(lemmatized_words))
            dict_list = []
            for site in site_list:
                dict_list.append(dict(site.vocab()))
        return dict_list
    else:
        return {'error': 500}

def scraper(querystring):
	results = scrape_google(querystring, 20, 'en')

	return filter_words_from_search(results)

# if __name__ == "__main__":
#   print(scraper("sgcodecampus.com"))

print(scraper("sgcodecampus"))
