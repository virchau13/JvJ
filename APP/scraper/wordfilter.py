import nltk
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

from searchscraper import scrape_google

tokenizer = RegexpTokenizer(r'\w+')

def filter_words_from_search(search_results):
    filteredwords = []
    punctuation = [",",".",":",";","'","-","!",'"',"-","|"]
    []
    for page in search_results:
        tokens = tokenizer.tokenize(page['title'])
        filteredtokens = [w for w in tokens if w not in nltk.corpus.stopwords.words('english')]
        filteredwords += [x for x in filteredtokens if x not in punctuation]

    filteredtext = Text(w.lower() for w in filteredwords)
    return filteredtext

results = scrape_google("sgcodecampus", 10, 'en')

filtered_results = filter_words_from_search(results)

results_vocab = filtered_results.vocab()

print(filtered_results)
print(results_vocab.freq)