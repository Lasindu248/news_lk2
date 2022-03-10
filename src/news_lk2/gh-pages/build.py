import os
import shutil

from utils import hashx, timex
from utils.xmlx import _

from news_lk2._utils import log
from news_lk2.analysis.ner import render_line
from news_lk2.analysis.paper import dedupe_by_title, get_articles
from news_lk2.core.filesys import DIR_REPO, DIR_ROOT, git_checkout

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')
MAX_DAYS_AGO = 7
FORMAT_LAST_UPDATED = '%I:%M%p, %A, %B %d, %Y (Sri Lanka Time)'
FORMAT_DATE_LINK_LABEL = '%b %d'


def clean():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')
    log.info(f'Cleaned {DIR_GH_PAGES}')


def render_meta():
    return _('meta', None, {'charset': 'utf-8'})


def render_link_styles(css_file='styles.css'):
    return _('link', None, {'rel': 'stylesheet', 'href': css_file})


def render_tts_script(article, h):
    text = '. '.join([article.title] + article.body_lines)
    return _('script', '''
function tts_%s() {
    let synth = window.speechSynthesis;
    synth.cancel();
    let text = '%s';
    let utterThis = new SpeechSynthesisUtterance(text);
    synth.speak(utterThis);
}
    ''' % (h, text))


def render_tts_button_only(h):
    return _(
        'button',
        '▶',
        {'onclick': 'tts_%s()' % (h), 'class': 'button-tts'},
    )


def render_tts_button(article):
    h = hashx.md5(article.title)
    return _('span', [
        render_tts_script(article, h),
        render_tts_button_only(h),
    ])


def render_article(article):
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
        article.body_lines,
    )), {'class': 'div-article'})


def build_paper():
    ut = timex.get_unixtime()
    ut_min = ut - MAX_DAYS_AGO * timex.SECONDS_IN.DAY

    articles = get_articles(ut_min=ut_min)
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
    ])
    html = _('html', [render_meta(), head, body])
    html_file = os.path.join(DIR_GH_PAGES, 'index.html')
    html.store(html_file)
    log.info(f'Stored {html_file} ({n_articles}  articles)')


def copy_css_file():
    src_css_file = 'src/news_lk2/gh-pages/styles.css'
    dest_css_file = os.path.join(DIR_GH_PAGES, 'styles.css')
    shutil.copy(src_css_file, dest_css_file)
    log.info(f'Copied {src_css_file} to {dest_css_file}')


def build():
    clean()
    git_checkout()
    build_paper()
    copy_css_file()


if __name__ == '__main__':
    build()
