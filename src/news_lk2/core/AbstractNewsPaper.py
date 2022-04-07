import os
from abc import ABC

from bs4 import BeautifulSoup
from utils import dt, www

from news_lk2._utils import log
from news_lk2.core.Article import Article
from news_lk2.core.filesys import get_article_file

MIN_ARTICLE_HTML_SIZE = 1_000
MIN_CHARS_IN_BODY_LINE = 60
MIN_WORDS_IN_BODY_LINE = 10


def is_valid_line(line):
    if len(line) < MIN_CHARS_IN_BODY_LINE:
        return False
    if len(line.split(' ')) < MIN_WORDS_IN_BODY_LINE:
        return False
    return True


def is_html_valid(html):
    if not html:
        log.warning('HTML is empty')
        return False

    if len(html) < MIN_ARTICLE_HTML_SIZE:
        log.warning('Insufficient HTML size')
        return False

    return True


class AbstractNewsPaper(ABC):
    @classmethod
    def use_selenium(cls):
        return False

    @classmethod
    def get_soup(cls, url):
        try:
            html = www.read(url, cached=True, use_selenium=cls.use_selenium())
        except Exception as e:
            log.error(str(e))
            return None

        if is_html_valid(html):
            return BeautifulSoup(html, 'html.parser')
        return None

    @classmethod
    def get_newspaper_id(cls):
        return dt.to_kebab(dt.camel_to_snake(cls.__name__))

    @classmethod
    def parse_article_urls(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_time_ut(cls, soup):
        raise NotImplementedError

    @classmethod
    def parse_title(cls, soup):
        h1_title = soup.find('h1')
        return h1_title.text.strip()

    @classmethod
    def parse_body_lines(cls, soup):
        raise NotImplementedError

    @classmethod
    def get_article_urls(cls):
        article_urls = []
        for index_url in cls.get_index_urls():
            soup = cls.get_soup(index_url)
            if soup:
                article_urls += cls.parse_article_urls(soup)

        newspaper_id = cls.get_newspaper_id()
        log.info(f'Found {len(article_urls)} articles for {newspaper_id}')
        return article_urls

    @classmethod
    def parse_and_store_article(cls, article_url):
        article_file = get_article_file(article_url)
        if os.path.exists(article_file):
            log.info(f'{article_file} already exists. Not parsing.')
            return

        soup = cls.get_soup(article_url)
        if not soup:
            log.warn(f'{article_file} has invalid HTML. Not parsing.')
            return
        article = Article(
            newspaper_id=cls.get_newspaper_id(),
            url=article_url,
            time_ut=cls.parse_time_ut(soup),
            title=cls.parse_title(soup),
            body_lines=list(filter(
                lambda line: is_valid_line(line),
                cls.parse_body_lines(soup),
            )),
        )
        article.store()

    @classmethod
    def scrape(cls):
        article_urls = cls.get_article_urls()
        for article_url in article_urls:
            cls.parse_and_store_article(article_url)
