import os
import shutil

from utils import filex, timex

from news_lk2._utils import log
from news_lk2.core import Article
from news_lk2.core.filesys import (DIR_REPO,
                                   get_article_files_for_date_and_newspaper,
                                   get_date_ids, get_newspapers_for_date)

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


def get_dir_papers():
    dir_papers = os.path.join(DIR_REPO, 'papers')
    if not os.path.exists(dir_papers):
        os.system(f'mkdir -p {dir_papers}')
    return dir_papers


def build_paper(days_ago):
    ut = timex.get_unixtime() - timex.SECONDS_IN.DAY * days_ago
    date_id = timex.get_date_id(ut)
    date = timex.get_date(ut)

    todays_articles = get_articles_for_dateid(date_id)

    n_todays_articles = len(todays_articles)
    md_lines = [
        f'# {date}',
        f'*{n_todays_articles} news articles*',
    ]
    for article in todays_articles:
        md_lines += [
            f'## [{article.time_only_str}] {article.title}',
            f'[{article.url}]',
        ]
        md_lines += article.body_lines

    md_file = os.path.join(
        get_dir_papers(),
        f'{date_id}.md',
    )
    filex.write(md_file, DELIM_MD.join(md_lines))
    log.info(f'Wrote {md_file}')
    return md_file


def copy_to_readme(md_file):
    readme_file = os.path.join(DIR_REPO, 'README.md')
    shutil.copy(md_file, readme_file)
    log.info(f'Wrote {readme_file}')


def run_daily_job():
    build_paper(2)
    build_paper(1)
    md_file = build_paper(0)
    copy_to_readme(md_file)
