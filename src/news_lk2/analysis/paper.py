

from news_lk2.core import Article
from news_lk2.core.filesys import get_article_files

DELIM_MD = '\n\n'


def get_articles():
    return list(reversed(sorted(map(
        Article.load,
        get_article_files(),
    ))))


def get_articles_for_date_id(date_id):
    return list(filter(
        lambda article: article.date_id == date_id,
        get_articles(),
    ))


def get_date_ids():
    return sorted(list(set(map(
        lambda article: article.date_id,
        get_articles(),
    ))))


def get_date_id_to_articles():
    articles = get_articles()
    date_id_to_articles = {}
    for article in articles:
        date_id = article.date_id
        if date_id not in date_id_to_articles:
            date_id_to_articles[date_id] = []
        date_id_to_articles[date_id].append(article)

    date_id_to_articles = dict(sorted(
        list(map(
            lambda item: [item[0], sorted(item[1])],
            date_id_to_articles.items(),
        )),
        key=lambda item: item[0],
    ))
    return date_id_to_articles
