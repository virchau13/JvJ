import nltk, string, pandas as pd, time, re
from nltk.text import Text
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

from searchscraper import scrape_google

#Creating tools for filtering
tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
lemmatize = WordNetLemmatizer().lemmatize
stop_words = set(stopwords.words('english'))



#Take title, description, content of search results and outputs them as a dictionary per site.
def filter_words_from_search(search_results):
    t0 = time.time()
    if (len(search_results) > 0):
        site_dict = dict([[page['link'], [dict(site.vocab()) for site in [Text(tex) for tex in [[lemmatize(t.lower()) for t in x if t not in string.punctuation and not t.isdigit() and lemmatize(t.lower()) not in stop_words and t != ""] for x in [tokenizer.tokenize(a['title'] + " " + a['description'] + " " + a['content']) for a in search_results]]]][page_num]] for page_num, page in enumerate(search_results)])
        context_list = dict([nltk.text.ContextIndex(tex) for tex in [[lemmatize(t.lower()) for t in x if t not in string.punctuation and not t.isdigit() and lemmatize(t.lower()) not in stop_words and t != ""] for x in [tokenizer.tokenize(a['title'] + " " + a['description'] + " " + a['content']) for a in search_results]]]
        t1 = time.time()
        print("Filter Time: " + str(t1 - t0))

        stuff_dict = defaultdict(lambda:defaultdict())
        for i in range(len(search_results)):
            stuff_dict["title"][search_results[i]["link"]] = search_results[i]["title"]
            stuff_dict["importance"][search_results[i]["link"]] = i+1
            stuff_dict["description"][search_results[i]["link"]] = search_results[i]["description"]

        return site_dict, stuff_dict, context_list
    else:
        return {'error': 404}

def get_scraped_urls(search_results):
    url_dict = {}
    if (len(search_results) > 0):
        for page_num in range(len(search_results)):
            page = search_results[page_num]
            urls = page['urls']
            url_dict[page['link']] = urls
    else:
        return {'error': 404}
    return url_dict

#Compiles search and filter into one command
def scraper(querystring, num_results):
	results = scrape_google(querystring, num_results, 'en')

	return filter_words_from_search(results)

#Outputs as a Panda DataFrame
def scraper_df(querystring, num_results):
    results, stuff, index = scraper(querystring, num_results)
    results = pd.DataFrame.from_dict(results, orient="index").fillna(0)
    #results.columns = ['Site' if x=='index' else x for x in results.columns]
    return results, stuff

def scrape_urls(querystring, num_results):
    results = scrape_google(querystring, num_results, 'en')

    return get_scraped_urls(results)

def get_related_words(word, context_index):
    similar_list = []
    for page in context_index:
        if (page.similar_words(word) != None):
            for similar in page.similar_words(word):
                similar_list.append(similar)
    return similar_list

if __name__ == "__main__":
    results, things, context_index = scraper("apple", 10)
    print(get_related_words("apple", context_index))