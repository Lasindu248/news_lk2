from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2.core import AbstractNewsPaper

URL_NEWS = 'https://island.lk/category/news/'
TIME_RAW_FORMAT = '%Y-%m-%d %I:%M %p'
MIN_WORDS_IN_BODY_LINE = 10


class IslandLk(AbstractNewsPaper):
    def get_article_d(self, soup):
        # time_ut
        meta_time = soup.find('meta', {'itemprop': 'dateModified'})
        time_ut = timex.parse_time(
            meta_time.get(
                'content',
                '').strip(),
            TIME_RAW_FORMAT)

        # title
        h1_title = soup.find('h1')
        title = h1_title.text.strip()

        # body lines
        header_inner = soup.find('div', {'id': 'mvp-content-wrap'})
        body_lines = list(map(
            lambda line: line.strip(),
            list(filter(
                lambda line: len(line.split(' ')) > MIN_WORDS_IN_BODY_LINE,
                header_inner.text.strip().split('\n'),
            ))
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
        for div in soup.find_all('li', {'class': 'mvp-blog-story-wrap'}):
            article_url = div.find('a').get('href')
            article_urls.append(article_url)

        return article_urls


if __name__ == '__main__':
    IslandLk().scrape()
