import os

from news_lk2.core.filesys import DIR_REPO, DIR_ROOT

DIR_GH_PAGES = os.path.join(DIR_ROOT, f'{DIR_REPO}-gh-pages')


def cleanup():
    os.system(f'rm -rf {DIR_GH_PAGES}')
    os.system(f'mkdir {DIR_GH_PAGES}')


def build():
    cleanup()


if __name__ == '__main__':
    build()
