import os
import shutil

from utils import timex
from utils.xmlx import _

from news_lk2._utils import log
from news_lk2.analysis.paper import get_articles_for_dateid
from news_lk2.core.filesys import (DIR_REPO, DIR_ROOT, get_date_ids,
                                   git_checkout)

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')
FORMAT_DATE_TITLE = '%A, %B %d, %Y'
N_BACKPOPULATE = 366


def clean():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')
    log.info(f'Cleaned {DIR_GH_PAGES}')


def render_link_styles(css_file='styles.css'):
    return _('link', None, {'rel': 'stylesheet', 'href': css_file})


def get_date_file_only(date_id):
    return f'{date_id}.html'


def parse_date_id(date_id):
    return timex.parse_time(date_id, timex.FORMAT_DATE_ID)


def render_date_link(date_id, is_current_date):
    ut = parse_date_id(date_id)
    date = timex.get_date(ut)
    class_name = 'a-date-link'
    if is_current_date:
        class_name += ' a-date-link-current'

    return _(
        'a',
        date,
        {
            'href': get_date_file_only(date_id),
            'class': class_name,
        },
    )


def render_link_box(label=None, current_date_id=None):
    date_ids = sorted(get_date_ids())
    date_ids.reverse()

    rendered_children = []
    prev_year_and_month = None
    for date_id in date_ids:
        year_and_month = date_id[:6]
        if prev_year_and_month and year_and_month != prev_year_and_month:
            rendered_children.append(_('br'))
        prev_year_and_month = year_and_month

        rendered_children.append(
            _('div', [render_date_link(date_id, date_id == current_date_id)]),
        )

    return _('div', rendered_children, {'class': 'div-link-box'})


def render_article(article):
    return _('div', [
        _('div', [
            _('a', article.url_domain, {'href': article.url}),
        ]),
        _('h3', [
            _('span', article.title),
            _('span', article.time_short_str, {'class': 'span-time-str-only'}),
        ]),
    ] + list(map(
        lambda line: _('p', line),
        article.body_lines,
    )), {'class': 'div-article'})


def build_paper_for_date(days_ago):
    ut = timex.get_unixtime() - timex.SECONDS_IN.DAY * days_ago
    date_id = timex.get_date_id(ut)

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
            _('div', rendered_articles,
                {'class': 'column-left'},
              ),
            _('div', [
                render_link_box(current_date_id=date_id),
            ], {'class': 'column-right'}),

        ], {'class': 'row'})
    ])
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
    # backpopulate
    for i in range(0, N_BACKPOPULATE):
        build_paper_for_date(i + 1)
    html_file = build_paper_for_date(0)
    copy_to_index(html_file)
    copy_css_file()


if __name__ == '__main__':
    build()
