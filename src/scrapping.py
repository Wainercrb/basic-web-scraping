import requests

from lxml.html import fromstring
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from itertools import cycle


def get_proxies():
    # website to get free proxies
    url = 'https://free-proxy-list.net/'

    response = requests.get(url)

    parser = fromstring(response.text)
    # using a set to avoid duplicate IP entries.
    proxies = set()

    for i in parser.xpath('//tbody/tr')[:10]:
        # to check if the corresponding IP is of type HTTPS
        if i.xpath('.//td[7][contains(text(),"yes")]'):

            # Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                            i.xpath('.//td[2]/text()')[0]])

            proxies.add(proxy)

    return proxies


proxies = get_proxies()
# to rotate through the list of IPs
proxyPool = cycle(proxies)
# insert the url of the website you want to scrape.
url = 'https://www.melon.com/mymusic/playlist/mymusicplaylistview_inform.htm?plylstSeq=473505374&memberKey=&ref=etc&snsGate=Y'
# request status code
status_code = None

for i in range(1, 11):
    print('Loop status code', status_code)
    if status_code == 200:
        break

    # Get a proxy from the pool
    proxy = next(proxyPool)
    print('Request #%d' % i)

    try:
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        response = requests.get(url, proxies={'http': proxy, 'https': proxy}, headers=headers)
        status_code = response.status_code
        parser = fromstring(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        print(soup)
        table = parser.xpath('//*[@id="songList"]')[0]
        print(table)
        print(response.json())
        break

    except requests.exceptions.RequestException as e:
        # One has to try the entire process as most
        # free proxies will get connection errors
        # We will just skip retries.
        print('Skipping.  Connection error', e)
    finally:
        print('The request ends')
