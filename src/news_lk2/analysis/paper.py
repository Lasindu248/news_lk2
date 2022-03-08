

from news_lk2.core import Article
from news_lk2.core.filesys import get_article_files

DELIM_MD = '\n\n'


def get_articles():
    return list(reversed(sorted(map(
        Article.load,
        get_article_files(),
    ))))


def get_articles_for_dateid(date_id):
    return list(filter(
        lambda article: article.date_id == date_id,
        get_articles(),
    ))


def get_date_ids():
    return sorted(list(set(map(
        lambda article: article.date_id,
        get_articles(),
    ))))
