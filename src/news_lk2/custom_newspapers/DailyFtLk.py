from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2.core import AbstractNewsPaper

URL_NEWS = 'https://www.ft.lk/ft-news/56'
TIME_RAW_FORMAT = '%A, %d %B %Y %H:%M'


class DailyFtLk(AbstractNewsPaper):
    def parse_time_ut(self, soup):
        span_time = soup.find('span', {'class': 'gtime'})
        return timex.parse_time(span_time.text.strip(), TIME_RAW_FORMAT)

    def parse_title(self, soup):
        h1_title = soup.find('h1')
        return h1_title.text.strip()

    def parse_body_lines(self, soup):
        header_inner = soup.find('header', {'class': 'inner-content'})
        return list(map(
            lambda line: line.strip(),
            header_inner.text.strip().split('\n'),
        ))

    def get_article_urls(self):
        html = www.read(URL_NEWS)
        soup = BeautifulSoup(html, 'html.parser')

        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-6'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        return article_urls
