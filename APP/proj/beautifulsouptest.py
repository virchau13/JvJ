from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import nltk
from nltk.corpus import stopwords

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def fetch_results(search_term, number_results, language_code):
    assert isinstance(search_term, str), 'Search term must be a string'
    assert isinstance(number_results, int), 'Number of results must be an integer'
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text

def parse_results(html, keyword):
    soup = BeautifulSoup(html, 'html.parser')

    found_results = []
    rank = 1
    result_block = soup.find_all('div', attrs={'class': 'g'})
    for result in result_block:

        link = result.find('a', href=True)
        title = result.find('h3', attrs={'class': 'r'})
        description = result.find('span', attrs={'class': 'st'})
        if link and title:
            link = link['href']
            title = title.get_text()
            if description:
                description = description.get_text()
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link': link})
                rank += 1
    return found_results

def scrape_google(search_term, number_results, language_code):
    keyword, html = fetch_results(search_term, number_results, language_code)
    results = parse_results(html, keyword)
    return results

results = scrape_google("sgcodecampus", 10, 'en')

print(results)
def getWordsInDoc(search):
    url = "https://www.google.com/search?source=hp&ei=pZM4W87oNpXc9QO1tpj4CQ&q=" + search + "&oq=" + search + "&gs_l=psy-ab.3..0j0i131k1j0l8.2723.2994.0.3159.4.4.0.0.0.0.194.318.0j2.2.0....0...1.1.64.psy-ab..2.2.318....0.5abtyOzQEKk"
    page = urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    strings = []
    words = []
    punctuation = [",",".",":",";","'","-","!",'"',"--","(",")","[","]","=","{","}","/","*","_"]

    for string in soup.stripped_strings:
        strings.append(string)

    for string in strings:
        for word in string.split():
            finishedword = ""
            for letter in list(word):
                if letter not in punctuation:
                    finishedword += letter
            if (finishedword != ""):
                words.append(finishedword)

    filteredWords = [w for w in words if w not in nltk.corpus.stopwords.words('english')]
    return filteredWords

def countWordsInDoc(doc, keyWord):
    wordCount = 0
    for word in doc:
        if (word == keyWord):
            wordCount += 1
    return wordCount

# print(getWordsInDoc("test"))
# print(countWordsInDoc(getWordsInDoc(page), "The"))

        