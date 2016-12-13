"""Handle web requests and parse markup"""

import random
import requests
from bs4 import BeautifulSoup

USER_AGENT = [
    "Mozilla/5.0 (Macintosh; Intel MAC OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0"
]

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8',
    'Accept-Enconding': 'gzip, deflate, sdch',
    'Connection': 'keep-alive',
    'User-Agent': USER_AGENT[random.randint(0, len(USER_AGENT)-1)]
}

SESSION = requests.Session()

def parse_markup(url, listings_per_page):
    """
    Send web requests using browser headers
    Returns BeautifulSoup object from parsed response markup
    """
    cookies = {"listing_results_per_page": "%s" % listings_per_page}
    response = SESSION.get(url, headers=HEADERS, cookies=cookies)
    if int(response.status_code) != 200:
        raise ValueError("Unsuccessful request: %s" % url)
    spider = BeautifulSoup(response.text, 'lxml')
    if spider is None:
        raise AttributeError("Markup could not be parsed from %s" % url)
    return spider