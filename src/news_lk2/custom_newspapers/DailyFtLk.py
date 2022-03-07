from utils import timex

from news_lk2.core import AbstractNewsPaper

TIME_RAW_FORMAT = '%A, %d %B %Y %H:%M'


class DailyFtLk(AbstractNewsPaper):
    @classmethod
    def get_index_urls(cls):
        return [
            'https://www.ft.lk/ft-news/56',
            'https://www.ft.lk/business-news/34',
        ]

    @classmethod
    def parse_article_urls(cls, soup):
        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-6'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)
        return article_urls

    @classmethod
    def parse_time_ut(cls, soup):
        span_time = soup.find('span', {'class': 'gtime'})
        return timex.parse_time(span_time.text.strip(), TIME_RAW_FORMAT)

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('header', {'class': 'inner-content'})
        return list(map(
            lambda line: line.strip(),
            header_inner.text.strip().split('\n'),
        ))
