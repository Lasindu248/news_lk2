import os

from utils.xmlx import _

from news_lk2._utils import log
from news_lk2.core.filesys import DIR_REPO, DIR_ROOT

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')


def clean():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')
    log.info(f'Cleaned {DIR_GH_PAGES}')


def build_index_html():
    body = _('body', [
        _('h1', 'News.lk'),
    ])
    html = _('html', [body])
    html_file = os.path.join(DIR_GH_PAGES, 'index.html')
    html.store(html_file)
    log.info(f'Stored {html_file}')


def build():
    clean()
    build_index_html()


if __name__ == '__main__':
    build()
