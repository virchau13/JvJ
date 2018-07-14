from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pathlib import Path
import requests, time, re, codecs, grequests, os
import user_agent

USER_AGENT = {'User-Agent': user_agent.generate_user_agent(os='mac',navigator='chrome')}

google_symbols = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '~', '\\']
symbol_dict = {}
for symbol_num in range(len(google_symbols)):
    symbol_dict[google_symbols[symbol_num]] = '%' + str(codecs.encode(google_symbols[symbol_num].encode('ascii'), 'hex')).replace('b', '').replace("'", '')

#Fetching results from google
def fetch_results(search_term, number_results, language_code):
    # t0 = time.time() 
    # escaped_search_term = search_term
    # for symbol, replacement in symbol_dict.items():
    #     escaped_search_term = escaped_search_term.replace(symbol, replacement)

    # google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    # response = requests.get(google_url, headers=USER_AGENT)
    # response.raise_for_status()
    # t1 = time.time()
    # print("Google results fetch time: " + str(t1 - t0))

    response = requests.get(
        "https://api.cognitive.microsoft.com/bing/v7.0/search",
        headers={"Ocp-Apim-Subscription-Key" : open(str(Path(os.getcwd()).parent.parent.parent) + '/api-key.txt', 'r').read()},
        params={'q': search_term, 'textDecorations': False, 'textFormat': 'HTML', 'count': number_results}
    )
    response.raise_for_status()
    results = response.json()['webPages']['value']
    for d in results:
        d.pop('about', None)
        d.pop('displayUrl', None)
        d.pop('deepLinks', None)
        d.pop('dateLastCrawled', None)

    return results

#Extracting title, description and link of sites found on the google site
# def parse_results(html, keyword):
#     soup = BeautifulSoup(html, 'html.parser')
#     found_results = []
#     rank = 1
#     result_block = soup.find_all('div', attrs={'class': 'g'})
#     for result in result_block:
#         link = result.find('a', href=True)
#         title = result.find('h3', attrs={'class': 'r'})
#         description = result.find('span', attrs={'class': 'st'})
#         if link and title:
#             link = link['href']
#             title = title.get_text()
#             if description:
#                 description = description.get_text()
#             else: 
#                 description = ""
#             if link != '#':
#                 found_results.append({'keyword': keyword, 'rank': rank, 'title': title, 'description': description, 'link': link.replace("/imgres?imgurl=", "")})
#                 rank += 1
#     t1 = time.time()
#     print("Parse time: " + str(t1 - t0))
#     return found_results

blacklist = ['a', 'title', 'p', 'input', 'u', 'body', 'html',
         'textarea', 'nobr', 'b', 'span', 'td', 'tr', 
         'br', 'table', 'form', 'img', 'head', 'meta', 
         'script', 'style', 'center', 'div']

#Scraping websites from google search for data
def scrape_google(search_term, number_results, language_code):
    t0 = time.time()
    results = fetch_results(search_term, number_results, language_code)
    t = time.time()
    response = grequests.map([grequests.get(u, timeout=0.5) for u in [x['url'] for x in results]])
    print('Website fetch time total:', time.time()-t, 'seconds')
    soup_list = [BeautifulSoup(res.text, 'html.parser') if res else BeautifulSoup("", 'html.parser') for res in response]
    for soup in soup_list:
        for tag in soup.findChildren():
            if (tag.name in blacklist):
                tag.decompose()
    soup_list = [soup.find_all(text=True) for soup in soup_list]
    contents = [[x.replace('\n', '').replace('\t', '').replace('\r', '') for x in tex if not x.parent.name in ['style', 'script', '[document]', 'head', 'title'] and not re.match('<!--.*-->', str(x.encode('utf-8')))] if tex != None else "" for tex in soup_list]
    for i in range(len(results)):
        results[i]['content'] = ' '.join(contents[i])
        results[i]['description'] = results[i].pop('snippet')
        results[i]['title'] = results[i].pop('name')
        results[i]['link'] = results[i].pop('url')
        results[i]["rank"] = i

    print('Everything done time:', time.time()-t0, 'seconds')
    return results

if __name__ == "__main__":
    print(scrape_google('xd', 15, 'en'))
