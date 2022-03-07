import os

from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2.core import AbstractNewsPaper

URL_BASE = 'http://dailynews.lk'
URL_NEWS = os.path.join(URL_BASE, 'category/local')
TIME_RAW_FORMAT = '%A, %B %d, %Y - %H:%M'
MIN_WORDS_IN_BODY_LINE = 10


class DailyNewsLk(AbstractNewsPaper):
    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('span', {'class': 'date-display-single'})
        return timex.parse_time(span_time.text.strip(), TIME_RAW_FORMAT)

    @classmethod
    def parse_body_lines(cls, soup):
        divs = soup.find_all('div', {'class': 'field-item'})
        body_lines = []
        for div in divs:
            body_lines += list(map(
                lambda line: line.strip(),
                list(filter(
                    lambda line: len(line.split(' ')) > MIN_WORDS_IN_BODY_LINE,
                    div.text.strip().split('\n'),
                ))
            ))
        return body_lines

    @classmethod
    def get_article_urls(cls):
        html = www.read(URL_NEWS)
        soup = BeautifulSoup(html, 'html.parser')

        article_urls = []
        for div in soup.find_all('li', {'class': 'views-row'}):
            article_url = os.path.join(
                URL_BASE,
                div.find('a').get('href')[1:],
            )
            article_urls.append(article_url)

        return article_urls


if __name__ == '__main__':
    DailyNewsLk.scrape()
