from bs4 import BeautifulSoup
from urllib.request import urlopen
import time, re, codecs, grequests, requests

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

google_symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '~', '\\']
symbol_dict = {}
for symbol_num in range(len(google_symbols)):
    symbol_dict[google_symbols[symbol_num]] = '%' + str(codecs.encode(google_symbols[symbol_num].encode('ascii'), 'hex')).replace('b', '').replace("'", '')

#Fetching results from google
def fetch_results(search_term, number_results, language_code):
    t0 = time.time() 
    escaped_search_term = search_term
    for symbol, replacement in symbol_dict.items():
        escaped_search_term = escaped_search_term.replace(symbol, replacement)

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()
    t1 = time.time()
    print("Google results fetch time: " + str(t1 - t0))

    return search_term, response.text

#Extracting title, description and link of sites found on the google site
def parse_results(html, keyword):
    t0 = time.time()
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
            else: 
                description = ""
            if link != '#':
                found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link': link.replace("/imgres?imgurl=", "")})
                rank += 1
    t1 = time.time()
    print("Parse time: " + str(t1 - t0))
    return found_results

#Scraping websites from google search for data
def scrape_google(search_term, number_results, language_code):
    keyword, html = fetch_results(search_term, number_results, language_code)
    results = parse_results(html, keyword)
    t0 = time.time()
    response = grequests.map([grequests.get(u) for u in [x['link'] for x in results]])
    print('Website fetch time total:', time.time()-t0, 'seconds')
    thing = [BeautifulSoup(res.text, 'html.parser').find_all(text=True) if res else None for res in response]
    contents = [[x.replace('\n', '').replace('\t', '').replace('\r', '') for x in tex if not x.parent.name in ['style', 'script', '[document]', 'head', 'title', 'span'] and not re.match('<!--.*-->', str(x.encode('utf-8')))] if tex else [] for tex in thing]
    for i in range(len(results)):
        results[i]['content'] = ' '.join(contents[i])
    print('Everything done time:', time.time()-t0, 'seconds')
    return results

if __name__ == "__main__":
    print(scrape_google('lol', 5, 'en'))