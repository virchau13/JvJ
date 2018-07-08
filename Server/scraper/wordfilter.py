import nltk
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer

from searchscraper import scrape_google

tokenizer = RegexpTokenizer(r'\w+')

lemmatizer = WordNetLemmatizer()

words = set(nltk.corpus.words.words())

def filter_words_from_search(search_results):
    site_list = []
    punctuation = [",",".",":",";","'","-","!",'"',"-","|","_"]

    for page_num in range(len(search_results)):
        filteredwords = []
        page = search_results[page_num]
        tokens = tokenizer.tokenize(page['title'])
        tokens += tokenizer.tokenize(page['description'])
        tokens += tokenizer.tokenize(page['content'])
        filteredtokens = [w for w in tokens if w not in nltk.corpus.stopwords.words('english')]
        filteredwords += [x for x in filteredtokens if (x not in punctuation and not x.isdigit())]
        lemmatized_words = []
        print(filteredwords)
        for word in filteredwords:
            word = "".join(w for w in nltk.wordpunct_tokenize(word) \
                if w.lower() in words or not w.isalpha())
            word = lemmatizer.lemmatize(word)
            lemmatized_words.append(word)

        site_list.append(Text(w.lower() for w in lemmatized_words))
        dict_list = []
        for site in site_list:
            dict_list.append(dict(site.vocab()))
    return dict_list

def scraper(querystring):
	results = scrape_google(querystring, 10, 'en')

	filtered_results = filter_words_from_search(results)

	return dict(results_vocab = filtered_results.vocab())

if __name__ == "__main__":
	print(scrape("sgcodecampus.com"))