import os

from utils import filex, jsonx, timex

from news_lk2._utils import log
from news_lk2.analysis.paper import get_articles, get_date_id_to_articles
from news_lk2.core.filesys import DIR_REPO, git_checkout
from news_lk2.custom_newspapers import newspaper_class_list

DELIM_MD = '\n' * 2
N_LATEST = 100


def build_readme_summary():
    date_id_to_articles = get_date_id_to_articles()
    md_lines = []
    md_lines.append('# news_lk2 (upload_data summary)')
    time_last_run = timex.format_current_date_with_timezone()
    md_lines.append(f'*Last run {time_last_run}*')

    total_n_articles = 0
    for date_id, articles in reversed(list(date_id_to_articles.items())):
        n_articles = len(articles)
        md_lines.append(f'* {date_id} - {n_articles} articles')
        total_n_articles += n_articles
    md_lines.append(f'* **TOTAL** - {total_n_articles} articles')

    md_file = os.path.join(DIR_REPO, 'README.md')
    filex.write(md_file, DELIM_MD.join(md_lines))
    log.info(f'Wrote {md_file}')


def build_articles_summary():
    articles = get_articles()
    data_list = []
    for article in articles:
        data_list.append(dict(
            newspaper_id=article.newspaper_id,
            time_ut=article.time_ut,
            title=article.title,
            url=article.url,
            file_name=article.file_name,
        ))
    data_list = sorted(data_list, key=lambda data: -data['time_ut'])

    articles_summary_file = os.path.join(DIR_REPO, 'articles.summary.json')
    jsonx.write(articles_summary_file, data_list)
    log.info(f'Wrote {articles_summary_file}')

    articles_summary_latest_file = os.path.join(
        DIR_REPO, 'articles.summary.latest.json')
    jsonx.write(articles_summary_latest_file, data_list[:N_LATEST])
    log.info(f'Wrote {articles_summary_latest_file}')


if __name__ == '__main__':
    git_checkout()
    for newspaper_class in newspaper_class_list:
        newspaper_class.scrape()
    build_readme_summary()
    build_articles_summary()
