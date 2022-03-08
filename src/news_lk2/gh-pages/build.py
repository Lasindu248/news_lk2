import os
import shutil

from utils import timex
from utils.xmlx import _

from news_lk2._utils import log
from news_lk2.analysis.paper import get_articles_for_dateid
from news_lk2.core.filesys import DIR_REPO, DIR_ROOT, git_checkout

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')


def clean():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')
    log.info(f'Cleaned {DIR_GH_PAGES}')


def render_link_styles(css_file='styles.css'):
    return _('link', None, {'rel': 'stylesheet', 'href': css_file})


def render_article(article):
    return _('div', [
        _('h2', f'[{article.time_only_str}] {article.title}'),
        _('div', [
            _('a', article.url, {'href': article.url}),
        ]),
    ] + list(map(
        lambda line: _('p', line),
        article.body_lines,
    )) + [
        _('hr'),
    ], {'class': 'div-article'})


def get_date_file_only(date_id):
    return f'{date_id}.html'


def parse_date_id(date_id):
    return timex.parse_time(date_id, timex.FORMAT_DATE)


def render_link_date(ut, label=None):
    date_id = timex.get_date_id(ut)
    date = timex.get_date(ut)
    if label is None:
        label = date
    return _('a', label, {'href': get_date_file_only(date_id)})


def build_paper_for_date(days_ago):
    ut = timex.get_unixtime() - timex.SECONDS_IN.DAY * days_ago
    date_id = timex.get_date_id(ut)
    date = timex.get_date(ut)

    days_articles = get_articles_for_dateid(date_id)
    n_days_articles = len(days_articles)
    log.info(f'Found {n_days_articles} articles for {date_id}')

    rendered_articles = list(map(
        render_article,
        days_articles,
    ))

    head = _('head', [render_link_styles()])
    body = _('body', [
        _('div', [
            render_link_date(ut - timex.SECONDS_IN.DAY),
            render_link_date(ut),
            render_link_date(ut + timex.SECONDS_IN.DAY),
        ]),
        _('h1', f'{date}'),
    ] + rendered_articles)
    html = _('html', [head, body])
    html_file = os.path.join(DIR_GH_PAGES, get_date_file_only(date_id))
    html.store(html_file)
    log.info(f'Stored {html_file}')

    return html_file


def copy_to_index(html_file):
    index_html_file = os.path.join(DIR_GH_PAGES, 'index.html')
    shutil.copy(html_file, index_html_file)
    log.info(f'Copied {html_file} to {index_html_file}')


def copy_css_file():
    src_css_file = 'src/news_lk2/gh-pages/styles.css'
    dest_css_file = os.path.join(DIR_GH_PAGES, 'styles.css')
    shutil.copy(src_css_file, dest_css_file)
    log.info(f'Copied {src_css_file} to {dest_css_file}')


def build():
    clean()
    git_checkout()
    build_paper_for_date(2)
    build_paper_for_date(1)
    html_file = build_paper_for_date(0)
    copy_to_index(html_file)
    copy_css_file()


if __name__ == '__main__':
    build()
