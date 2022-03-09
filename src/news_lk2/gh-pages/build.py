import os
import shutil

from utils import timex
from utils.xmlx import _

from news_lk2._utils import log
from news_lk2.analysis.paper import get_date_id_to_articles, get_date_ids
from news_lk2.core.filesys import DIR_REPO, DIR_ROOT, git_checkout

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')
N_BACKPOPULATE = 28
FORMAT_LAST_UPDATED = '%I:%M%p, %A, %B %d, %Y (Sri Lanka Time)'
FORMAT_DATE_LINK_LABEL = '%b %d'


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
    label = timex.format_time(ut, FORMAT_DATE_LINK_LABEL)
    class_name = 'a-date-link'
    if is_current_date:
        class_name += ' a-date-link-current'

    return _(
        'a',
        [
            _('time', label, {'datetime': timex.format_time(ut)}),
        ],
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
        _('h3', article.title),
        _('div', [
            _('span', [
                _(
                    'time',
                    article.time_short_str,
                    {'datetime': timex.format_time(article.time_ut)},
                ),
            ], {'class': 'span-time-str-only'}),
            _('span', ' · ', {'class': 'span-seperator'}),
            _('span',
                f'{article.reading_time_min:.0f} min read',
                {'class': 'span-reading-time'},
              ),
        ]),
    ] + list(map(
        lambda line: _('p', line),
        article.body_lines,
    )), {'class': 'div-article'})


def build_paper(date_id, days_articles):
    days_articles.reverse()
    ut = timex.get_unixtime()
    n_days_articles = len(days_articles)

    rendered_articles = list(map(
        render_article,
        days_articles,
    ))

    time_last_updated = timex.format_time(
        ut,
        FORMAT_LAST_UPDATED,
        timex.TIMEZONE_OFFSET_LK,
    )
    last_updated_text = f'Last updated {time_last_updated}'

    head = _('head', [render_link_styles()])
    body = _('body', [
        _('div', [
            _('div', [
                _(
                    'time',
                    last_updated_text,
                    {'datetime': timex.format_time(ut)},
                )
            ], {'class': 'div-last-updated'}),
            _('div', rendered_articles,
                {'class': 'column-left'},
              ),
            _('div', [
                render_link_box(current_date_id=date_id),
            ], {'class': 'column-right'}),

        ], {'class': 'row'})
    ])
    html = _('html', [head, body])
    file_only = get_date_file_only(date_id)
    html_file = os.path.join(DIR_GH_PAGES, file_only)
    html.store(html_file)
    log.info(f'Stored {html_file} ({n_days_articles}  articles)')

    return file_only


def build_index_file(html_file):
    head = _('head', [
        _('meta', None, {
            'http-equiv': 'refresh',
            'content': f'0; URL={html_file}',
        }),
    ])
    html = _('html', [head])
    html_file = os.path.join(DIR_GH_PAGES, 'index.html')
    html.store(html_file)
    log.info(f'Stored {html_file}')


def copy_css_file():
    src_css_file = 'src/news_lk2/gh-pages/styles.css'
    dest_css_file = os.path.join(DIR_GH_PAGES, 'styles.css')
    shutil.copy(src_css_file, dest_css_file)
    log.info(f'Copied {src_css_file} to {dest_css_file}')


def build():
    clean()
    git_checkout()
    html_file = None
    for date_id, articles in get_date_id_to_articles().items():
        html_file = build_paper(date_id, articles)
    build_index_file(html_file)
    copy_css_file()


if __name__ == '__main__':
    build()
