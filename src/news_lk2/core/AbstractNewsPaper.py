from abc import ABC

from bs4 import BeautifulSoup
from utils import dt, www

from news_lk2._utils import log
from news_lk2.core.Article import Article


class AbstractNewsPaper(ABC):
    @classmethod
    def parse_time_ut(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_title(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_body_lines(cls, soup):
        raise NotImplementedError

    @classmethod
    def get_article_urls(cls):
        raise NotImplementedError

    @classmethod
    def get_newspaper_id(cls):
        return dt.to_kebab(dt.camel_to_snake(cls.__name__))

    @classmethod
    def scrape(cls):
        article_urls = cls.get_article_urls()
        newspaper_id = cls.get_newspaper_id()
        log.info(f'Found {len(article_urls)} articles for {newspaper_id}')

        for article_url in article_urls:
            html = www.read(article_url)
            soup = BeautifulSoup(html, 'html.parser')

            article = Article(
                newspaper_id=newspaper_id,
                url=article_url,
                time_ut=cls.parse_time_ut(soup),
                title=cls.parse_title(soup),
                body_lines=cls.parse_body_lines(soup),
            )
            article.store()
