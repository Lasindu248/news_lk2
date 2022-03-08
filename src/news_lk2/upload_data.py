import os

from utils import filex, timex

from news_lk2._utils import log
from news_lk2.analysis.paper import get_date_id_to_articles
from news_lk2.core.filesys import DIR_REPO, git_checkout
from news_lk2.custom_newspapers import newspaper_class_list

DELIM_MD = '\n' * 2


def build_readme_summary():
    date_id_to_articles = get_date_id_to_articles()
    md_lines = []
    md_lines.append('# news_lk2 (upload_data summary)')
    time_last_run = timex.format_current_date_with_timezone()
    md_lines.append(f'*Last run {time_last_run}*')

    for date_id, articles in reversed(list(date_id_to_articles.items())):
        n_articles = len(articles)
        md_lines.append(f'* {date_id} - {n_articles} articles')

    md_file = os.path.join(DIR_REPO, 'README.md')
    filex.write(md_file, DELIM_MD.join(md_lines))
    log.info(f'Wrote {md_file}')


if __name__ == '__main__':
    git_checkout()
    for newspaper_class in newspaper_class_list:
        newspaper_class.scrape()
    build_readme_summary()
