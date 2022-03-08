import os
import shutil

from utils import filex, timex

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.filesys import (DIR_REPO,
                                   get_article_files_for_date_and_newspaper,
                                   get_date_ids, get_newspapers_for_date,
                                   git_checkout)

DELIM_MD = '\n\n'


def get_articles_for_dateid(date_id):
    date_ids = get_date_ids()
    if date_id not in date_ids:
        log.warning(f'No articles for ({date_id}). Aborting')
        return []

    newspaper_ids = get_newspapers_for_date(date_id)
    article_list = []
    for newspaper_id in newspaper_ids:
        article_files = get_article_files_for_date_and_newspaper(
            date_id,
            newspaper_id,
        )
        article_list += list(map(
            Article.load,
            article_files,
        ))

    article_list.sort()
    article_list.reverse()
    return article_list
