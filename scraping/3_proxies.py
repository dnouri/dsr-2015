# WARNING: Using this script will violate Google's terms of service.
#          So don't use it.

from multiprocessing.dummy import Pool as ThreadPool
import pickle
import random
from time import sleep
from time import time
import urllib
import urlparse

from newspaper import Article
from pyquery import PyQuery as pq
import requests

GOOGLE_NEWS_URL = 'https://www.google.com/search?tbm=nws&q={}'
HEADERS = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # 'accept-encoding': 'gzip,deflate,sdch',
    # 'accept-language': 'en-US,en;q=0.8,de;q=0.6',
    # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36',
    }

# http://proxylist.hidemyass.com/
http_proxies = [
    'http://196.201.217.49:4012',
    'http://218.108.170.169:80',
    'http://118.96.138.7:8080',
    ]

https_proxies = [
    'http://118.97.194.49:8080',
    'http://46.10.166.143:8080',
    'http://111.161.126.85:80',
    ]

search_terms = [
    'brazil',
    'japan',
    # 'north korea',
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
    urls = []
    for anchor in doc(".g a"):
        href = anchor.attrib['href']
        query = urlparse.parse_qs(urlparse.urlparse(href).query)
        urls.append(query['q'][0])
    return urls


def get_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article


def get_articles_urls_for(term):
    url = GOOGLE_NEWS_URL.format(urllib.quote(term))
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
        article_urls = get_articles_urls_for(term)
        articles = pool.map(get_article, article_urls)
        terms_to_articles[term] = articles

    print("Fetching articles took {:.1f} seconds".format(time() - t0))

    for term in search_terms:
        articles = terms_to_articles[term]
        print("Articles for {} ({}):".format(term, len(articles)))
        for article in articles:
            print(u"  == {} ==".format(article.title))
            print(u"  {}...".format(article.text[:70]))
            print(u"  - {}".format(article.url))
            print

    with open('articles.pickle', 'wb') as f:
        pickle.dump(terms_to_articles, f)


main()
