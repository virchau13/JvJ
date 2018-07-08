import nltk
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
    punctuation = [",",".",":",";","'","-","!",'"',"-","|","_",""]
    if (len(search_results) > 0):
        for page_num in range(len(search_results)):
            filteredwords = []
            page = search_results[page_num]
            tokens = tokenizer.tokenize(page['title'])
            tokens += tokenizer.tokenize(page['description'])
            tokens += tokenizer.tokenize(page['content'])
            filteredtokens = [w for w in tokens]
            filteredwords += [x for x in filteredtokens if (x not in punctuation and not x.isdigit())]
            lemmatized_words = []
            for word in filteredwords:
                filtered_word = regex.sub('', word).lower()
                lemmatized = lemmatizer.lemmatize(filtered_word)
                if lemmatized not in stop_words and lemmatized != "":
                    lemmatized_words.append(lemmatized)

            site_list.append(Text(lemmatized_words))
            dict_list = []
            for site in site_list:
                dict_list.append(dict(site.vocab()))
        return dict_list
    else:
        return {'error': 500}

def scraper(querystring):
	results = scrape_google(querystring, 10, 'en')

	return filter_words_from_search(results)

# if __name__ == "__main__":
#   print(scraper("sgcodecampus.com"))

print(scraper("*"))
