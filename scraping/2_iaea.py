from datetime import date
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from time import time

import matplotlib.pyplot as plt
from pandas import DataFrame
from pyquery import PyQuery as pq

# https://pythonhosted.org/pyquery/scrap.html

MAIN_URL = 'http://www-news.iaea.org/EventList.aspx?ps=100&pno=0'


def get_news_links(url):
    doc = pq(url).make_links_absolute()
    result = []
    for anchor in doc("h4 a"):
        result.append(anchor.attrib['href'])
    return result


def get_event_info(url):
    doc = pq(url)

    date_posted = doc("#MainContent_lblPostedOn").text()[11:]
    date_incident = doc("#MainContent_lblEventDateValue").text()
    date_posted = datetime.strptime(date_posted, "%d %B %Y").date()
    date_incident = datetime.strptime(date_incident, "%d %B %Y").date()
    location = doc("#MainContent_lblEventLocationValue").text()

    return {
        'title': doc("#MainContent_lblEventExpertTitleValue").text(),
        'date_posted': date_posted,
        'date_incident': date_incident,
        'country': location.split(',', 1)[0].strip(),
        'location': location.split(',', 1)[1].strip(),
        'type': doc("#MainContent_lblNoticeEventCategoryValue").text(),
        'ines_rating': int(doc("#MainContent_lblINESRatingValue").text()[0]),
        'description': doc("#MainContent_lblEventDescriptionValue").text(),
        'beyond_authorized_limits': 'YOUR CODE HERE',
        'public_exposure': 'YOUR CODE HERE',
        'contact_name': 'YOUR CODE HERE',
        'contact_email': 'YOUR CODE HERE',
        }


def test_get_event_info():
    url = ('http://www-news.iaea.org/ErfView.aspx'
           '?mId=c0b8cf3a-8f1d-4601-8b5b-8254efc33411')
    info = get_event_info(url)

    assert info['title'].startswith('Exposure of a temporary worker in excess')
    assert info['date_posted'] == date(2014, 10, 17)
    assert info['date_incident'] == date(2014, 5, 17)
    assert info['country'] == 'India'
    assert info['location'] == 'TARAPUR-4'
    assert info['type'] == 'Power Reactor'
    assert info['ines_rating'] == 1
    assert info['description'].startswith('At  TAPS-4, irradiated Cobalt Self')
    assert info['description'].endswith('of 15 mSv  for a temporary worker.')
    assert info['beyond_authorized_limits'] is False
    assert info['public_exposure'] is False
    assert info['worker_exposure'] is True
    # ...
    assert info['contact_name'] == 'Swaminathan Duraisamy'
    assert info['contact_email'] == 'durai@aerb.gov.in'


def main():
    urls = get_news_links(MAIN_URL)
    pool = ThreadPool(4)

    t0 = time()
    results = pool.map(get_event_info, urls)
    print("Scraping took {:.2f} seconds".format(time() - t0))

    # Make a DataFrame out of the results:
    df = DataFrame(results)

    # Now try some plotting:
    df['country'].value_counts().plot(kind='bar')
    plt.show()

    plt.plot_date(df.date_incident, df.ines_rating)
    plt.ylim(-0.5, df.ines_rating.max() + 0.5)
    plt.show()


if __name__ == '__main__':
    # test_get_event_info()
    main()
