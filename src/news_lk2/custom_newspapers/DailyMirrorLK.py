from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2._utils import log
from news_lk2.core import AbstractNewsPaper

URL_NEWS = 'https://www.dailymirror.lk/latest-news/342'
TIME_RAW_FORMAT = '%d %B %Y %I:%M %p'
NEWSPAPER_NAME = 'lk_daily_mirror'


class DailyMirrorLK(AbstractNewsPaper):
    def get_newspaper_id(self):
        return 'daily-mirror-lk'

    def get_article_d(self, url):
        html = www.read(url)
        soup = BeautifulSoup(html, 'html.parser')

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

        n_articles = 0
        article_urls = []
        for div in soup.find_all('div', {'class': 'col-md-8'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        n_articles = len(article_url)
        log.info(f'Got {n_articles} off {URL_NEWS}')
        return article_urls
