from bs4 import BeautifulSoup
from utils import dt, www
from news_lk2.core.Article import Article

class AbstractNewsPaper:
    def get_article_d(self):
        raise NotImplementedError

    def get_article_urls(self):
        raise NotImplementedError

    @property
    def newspaper_id(self):
        return dt.to_kebab(dt.camel_to_snake(self.__class__.__name__))

    def scrape(self):
        article_urls = self.get_article_urls()
        for article_url in article_urls:
            html = www.read(article_url)
            soup = BeautifulSoup(html, 'html.parser')
            d = self.get_article_d(soup)

            article = Article(
                newspaper_id=self.newspaper_id,
                url=article_url,
                time_ut=d['time_ut'],
                title=d['title'],
                body_lines=d['body_lines'],
            )
            article.store()
