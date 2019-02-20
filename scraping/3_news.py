# WARNING: Using this script will violate Google's terms of service.
#          So don't use it.

from multiprocessing.dummy import Pool as ThreadPool
import pickle
import random
from time import sleep
from time import time
import urllib
import urllib.parse

from newspaper import Article
from pyquery import PyQuery as pq
import requests

GOOGLE_NEWS_URL = 'https://www.google.com/search?tbm=nws&q={}'
HEADERS = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'accept-encoding': 'gzip,deflate,sdch',
    'accept-language': 'en-US,en;q=0.8,de;q=0.6',
    # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36',
    }

http_proxies = [
    'http://198.27.67.35:3128',
    'http://178.128.47.62:3128',
    ]

https_proxies = [
    'http://158.69.243.155:18888',
    'http://200.255.122.174:8080',
    ]

search_terms = [
    'brazil',
    'north korea',
    # 'japan',
    # 'pakistan',
    # 'palestine',
    # 'syria',
    ]


def get_random_proxies():
    result = {
        'http': random.choice(http_proxies),
        'https': random.choice(https_proxies),
        }
    print(result)
    return result


def get_urls_from_search_results(doc):
    urls = set()
    for anchor in doc(".g a"):
        href = anchor.attrib['href']
        query = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
        urls.add(query['q'][0])
    return urls


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    del article.clean_doc
    del article.clean_top_node
    del article.doc
    del article.top_node
    return article


def get_article_urls_for(term):
    url = GOOGLE_NEWS_URL.format(urllib.parse.quote(term))
    while True:
        # resp = requests.get(url, headers=HEADERS, proxies=get_random_proxies())
        resp = requests.get(url, headers=HEADERS)
        if resp.status_code == 200:
            return get_urls_from_search_results(pq(resp.text))
        sleep(1)


def main():
    pool = ThreadPool(4)
    terms_to_articles = {}

    t0 = time()

    for term in search_terms:
        print("Getting articles for {}...".format(term))
        article_urls = get_article_urls_for(term)
        articles = pool.map(get_article, article_urls)
        terms_to_articles[term] = articles

    print("Fetching articles took {:.1f} seconds".format(time() - t0))

    for term in search_terms:
        articles = terms_to_articles[term]
        print("Articles for '{}' ({}):".format(term, len(articles)))
        for article in articles:
            print("  - {}".format(article.title))
            print("  - text:  {}...".format(article.text[:70]))
            print("  - url:   {}".format(article.url))
            print()

    with open('articles.pickle', 'wb') as f:
        pickle.dump(terms_to_articles, f)


main()
