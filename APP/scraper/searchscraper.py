from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import requests

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

def fetch_results(search_term, number_results, language_code):
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

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def scrape_google(search_term, number_results, language_code):

    keyword, html = fetch_results(search_term, number_results, language_code)
    results = parse_results(html, keyword)

    for site in range(len(results)): 
        response = requests.get(results[site]['link'], headers=USER_AGENT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        filtered_site = ""
        
        site_content = soup.find_all(text=True)
        for text in site_content:
            if (not text.parent.name in ['style', 'script', '[document]', 'head', 'title'] and not re.match('<!--.*-->', str(text.encode('utf-8')))):
                text = text.replace('\n', '')
                text = text.replace('\r', '')
                text = text.replace('\t', '')
                filtered_site += (text + " ").rstrip()

                
        results[site]['content'] = filtered_site

    return results

print(scrape_google("sgcodecampus", 10, 'en'))