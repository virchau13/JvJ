from bs4 import BeautifulSoup
import re
from urllib.request import urlopen
import requests
import time

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

#Fetching results from google
def fetch_results(search_term, number_results, language_code):
    t0 = time.time() 
    escaped_search_term = search_term.replace('+', '%2B').replace(' ', '+').replace('&', '%26')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()
    t1 = time.time()
    print("Fetch Time: " + str(t1 - t0))

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
    print("Parse Time: " + str(t1 - t0))
    return found_results

#Scraping websites from google search for data
def scrape_google(search_term, number_results, language_code):
    t0 = time.time()
    try:
        keyword, html = fetch_results(search_term, number_results, language_code)
        results = parse_results(html, keyword)

        #Checking if site is accessible (CloudFlare Protection)
        for site in range(len(results)): 
            t2 = time.time()
            try:
                response = requests.get(results[site]['link'], headers=USER_AGENT, verify=False)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                site_content = soup.find_all(text=True)
            except requests.HTTPError as err:
                # if (err.response.status_code == 503):
                site_content = ""

            filtered_site = ""
        #Taking all data from  website and removing \ symbols (newline, etc)
            # for text in site_content:
            #     if (not text.parent.name in ['style', 'script', '[document]', 'head', 'title'] and not re.match('<!--.*-->', str(text.encode('utf-8')))):
            #         text = text.replace('\n', '').replace('\r', '').replace('\t', '')  
            results[site]['content'] = filtered_site
            t3 = time.time()
            print("Scrape Time: " + str(t3 - t2) + " Rank: " + str(results[site]['rank']))
        t1 = time.time()
        print("Scrape Time: " + str(t1 - t0))
        return results
    #Error Catching
    except AssertionError:
        raise Exception("Incorrect arguments parsed to function")
    except requests.HTTPError:
        raise Exception("You appear to have been blocked by Google")
    except requests.RequestException:
        raise Exception("Appears to be an issue with your connection")