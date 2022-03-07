from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2.core import AbstractNewsPaper

URL_NEWS = 'https://island.lk/category/news/'
TIME_RAW_FORMAT = '%Y-%m-%d %I:%M %p'
MIN_WORDS_IN_BODY_LINE = 10


class IslandLk(AbstractNewsPaper):
    @classmethod
    def parse_time_ut(cls, soup):
        meta_time = soup.find('meta', {'itemprop': 'dateModified'})
        return timex.parse_time(
            meta_time.get(
                'content',
                '').strip(),
            TIME_RAW_FORMAT)

    @classmethod
    def parse_body_lines(cls, soup):
        header_inner = soup.find('div', {'id': 'mvp-content-wrap'})
        return list(map(
            lambda line: line.strip(),
            list(filter(
                lambda line: len(line.split(' ')) > MIN_WORDS_IN_BODY_LINE,
                header_inner.text.strip().split('\n'),
            ))
        ))

    @classmethod
    def get_article_urls(cls):
        html = www.read(URL_NEWS)
        soup = BeautifulSoup(html, 'html.parser')

        article_urls = []
        for div in soup.find_all('li', {'class': 'mvp-blog-story-wrap'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        return article_urls
