from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2.core import AbstractNewsPaper

URL_NEWS = 'https://www.ft.lk/ft-news/56'
TIME_RAW_FORMAT = '%A, %d %B %Y %H:%M'


class DailyFtLk(AbstractNewsPaper):
    def get_article_d(self, soup):
        # time_ut
        span_time = soup.find('span', {'class': 'gtime'})
        time_ut = timex.parse_time(span_time.text.strip(), TIME_RAW_FORMAT)

        # title
        h1_title = soup.find('h1')
        title = h1_title.text.strip()

        # body lines
        header_inner = soup.find('header', {'class': 'inner-content'})
        body_lines = list(map(
            lambda line: line.strip(),
            header_inner.text.strip().split('\n'),
        ))

        return dict(
            time_ut=time_ut,
            title=title,
            body_lines=body_lines,
        )

    def get_article_urls(self):
        html = www.read(URL_NEWS)
        soup = BeautifulSoup(html, 'html.parser')

        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-6'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        return article_urls
