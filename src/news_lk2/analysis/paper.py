from news_lk2.core import Article
from news_lk2.core.filesys import (get_article_files_for_date_and_newspaper,
                                   get_date_ids, get_newspapers_for_date,
                                   git_checkout)

if __name__ == '__main__':
    git_checkout()
    date_ids = get_date_ids()
    for date_id in date_ids:
        print(date_id)
        newspaper_names = get_newspapers_for_date(date_id)
        for newspaper_name in newspaper_names:
            print(' ' * 2, newspaper_name)
            article_files = get_article_files_for_date_and_newspaper(
                date_id,
                newspaper_name,
            )
            for article_file in article_files:
                article = Article.load(article_file)
                print(' ' * 4, article.title)
