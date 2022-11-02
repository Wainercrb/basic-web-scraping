import requests

from lxml.html import fromstring

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
        print('the proxy', proxy)
