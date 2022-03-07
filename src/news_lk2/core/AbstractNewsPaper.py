from bs4 import BeautifulSoup
from utils import dt, www

from news_lk2._utils import log
from news_lk2.core.Article import Article


class AbstractNewsPaper:
    def parse_time_ut(self, soup):
        raise NotImplementedError

    def parse_title(self, soup):
        raise NotImplementedError

    def parse_body_lines(self, soup):
        raise NotImplementedError

    def get_article_urls(self):
        raise NotImplementedError

    @property
    def newspaper_id(self):
        return dt.to_kebab(dt.camel_to_snake(self.__class__.__name__))

    def scrape(self):
        article_urls = self.get_article_urls()
        log.info(f'Found {len(article_urls)} articles for {self.newspaper_id}')

        for article_url in article_urls:
            html = www.read(article_url)
            soup = BeautifulSoup(html, 'html.parser')

            article = Article(
                newspaper_id=self.newspaper_id,
                url=article_url,
                time_ut=self.parse_time_ut(soup),
                title=self.parse_title(soup),
                body_lines=self.parse_body_lines(soup),
            )
            article.store()
