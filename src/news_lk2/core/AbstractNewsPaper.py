
from news_lk2.core.Article import Article

class AbstractNewsPaper:
    def get_newspaper_id():
        raise NotImplementedError

    def get_article_d(self):
        raise NotImplementedError

    def get_article_urls(self):
        raise NotImplementedError

    def scrape(self):
        article_urls = self.get_article_urls()
        for article_url in article_urls:
            d = self.get_article_d(article_url)
            article = Article(
                newspaper_id=self.get_newspaper_id(),
                url=article_url,
                time_ut=d['time_ut'],
                title=d['title'],
                body_lines=d['body_lines'],
            )
            article.store()
