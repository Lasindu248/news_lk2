import os
import shutil

from utils import timex
from utils.xmlx import _

from news_lk2._constants import TEST_MODE
from news_lk2._utils import log
from news_lk2.analysis.ner import render_line
from news_lk2.analysis.paper import (dedupe_by_title, get_articles,
                                     split_body_lines)
from news_lk2.core.filesys import DIR_REPO, DIR_ROOT, git_checkout

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')
MAX_DAYS_AGO = 1 if TEST_MODE else 7
FORMAT_LAST_UPDATED = '%I:%M%p, %A, %B %d, %Y (Sri Lanka Time)'
FORMAT_DATE_LINK_LABEL = '%b %d'


def clean():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')
    log.info(f'Cleaned {DIR_GH_PAGES}')


def render_meta():
    return _('meta', None, {'charset': 'utf-8'})


def render_javascript():
    return _(
        'script',
        ' ',
        {'type': 'text/javascript', 'src': 'index.js'},
    )


def render_link_styles(css_file='styles.css'):
    return _('link', None, {'rel': 'stylesheet', 'href': css_file})


def render_tts_button(article):
    id = f'button-tts-{article.url_hash}'
    title = article.title
    body = '. '.join(article.body_lines)
    return _(
        'button',
        '⏯︎',
        {
            'onclick': '''tts('%s', '%s', '%s')''' % (id, title, body),
            'class': 'button-tts',
            'id': id,
        },
    )


def render_article(article):
    before_lines, after_lines = split_body_lines(article.body_lines)
    return _('div', [
        _('div', [
            _(
                'a',
                article.url_domain,
                {'href': article.url, 'class': 'a-newspaper'}
            ),
        ]),
        _('h3', [render_line(article.title)]),
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
            render_tts_button(article),
        ]),
    ] + list(map(
        lambda line: _('p', [render_line(line)]),
        before_lines + ['...'],
    )), {'class': 'div-article'})


def build_paper():
    ut = timex.get_unixtime()
    ut_min = ut - MAX_DAYS_AGO * timex.SECONDS_IN.DAY

    articles = get_articles(ut_min=ut_min)
    if TEST_MODE:
        articles = articles[:5]
    articles = dedupe_by_title(articles)
    articles.reverse()

    n_articles = len(articles)

    rendered_articles = list(map(
        render_article,
        articles,
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
            _(
                'time',
                last_updated_text,
                {'datetime': timex.format_time(ut)},
            )
        ], {'class': 'div-last-updated'}),
        _('div', rendered_articles),
        render_javascript(),
    ])
    html = _('html', [render_meta(), head, body])
    html_file = os.path.join(DIR_GH_PAGES, 'index.html')
    html.store(html_file)
    log.info(f'Stored {html_file} ({n_articles}  articles)')


def copy_files():
    for file_only in ['styles.css', 'index.js']:
        src_file = os.path.join('src/news_lk2/gh-pages', file_only)
        dest_file = os.path.join(DIR_GH_PAGES, file_only)
        shutil.copy(src_file, dest_file)
        log.info(f'Copied {src_file} to {dest_file}')


def build():
    if not TEST_MODE:
        clean()
        git_checkout()
        build_paper()
    copy_files()


if __name__ == '__main__':
    build()
