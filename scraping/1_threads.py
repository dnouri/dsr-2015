from multiprocessing.dummy import Pool as ThreadPool
from time import time

import requests


urls = [
    'http://python.org/about',
    'http://pymotw.com/2/collections/deque.html',
    'https://docs.python.org/2/library/multiprocessing.html',
    'http://pythong.org/',
    'http://pythong.org/morehoff.html',
    'http://en.wikipedia.org/wiki/Portal:Current_events',
    'http://en.wikipedia.org/wiki/Main_Page',
    'http://pymotw.com/2/',
    'http://www-news.iaea.org/EventList.aspx?ps=100&pno=0',
    ]


def timeit(func):
    def decorator(*args, **kwargs):
        t0 = time()
        result = func(*args, **kwargs)
        td = time() - t0
        msg = "Time spent in {}: {:.3f} seconds".format(func.__name__, td)
        print(msg)
        return result
    return decorator


@timeit
def nothreads(urls):
    results = []
    for url in urls:
        results.append(requests.get(url))
    return results


@timeit
def twothreads(urls):
    pool = ThreadPool(2)
    return pool.map(requests.get, urls)


@timeit
def eightthreads(urls):
    pool = ThreadPool(8)
    return pool.map(requests.get, urls)


nothreads(urls)
twothreads(urls)
result = eightthreads(urls)

print(result[0].text[:100])
