import os
import shutil

from utils import hashx, timex

from news_lk2._utils import log

REPO_NAME = 'news_lk2'
GIT_REPO_URL = f'https://github.com/nuuuwan/{REPO_NAME}.git'
DIR_ROOT = '/tmp'
DIR_REPO = os.path.join(DIR_ROOT, REPO_NAME)
SALT = '5568445278803347'
HASH_LENGTH = 8
IGNORE_LIST = ['.git', '.gitignore', '.DS_Store']


def get_dir_article_root():
    return os.path.join(
        DIR_REPO,
        'articles',
    )


def get_dir_date(date_id):
    return os.path.join(
        get_dir_article_root(),
        date_id,
    )


def get_dir_date_and_newspaper(date_id, newspaper_id):
    return os.path.join(
        get_dir_date(date_id),
        newspaper_id,
    )


def get_article_file_only(url):
    h = hashx.md5(url + SALT)[:HASH_LENGTH]
    return f'{h}.json'


def get_article_file(time_ut, newspaper_id, url):
    date_id = timex.get_date_id(time_ut)

    dir_date_and_newspaper = get_dir_date_and_newspaper(
        date_id,
        newspaper_id,
    )
    if not os.path.exists(dir_date_and_newspaper):
        os.system(f'mkdir -p {dir_date_and_newspaper}')
    return os.path.join(
        dir_date_and_newspaper,
        get_article_file_only(url),
    )


def git_checkout():
    if os.path.exists(DIR_REPO):
        shutil.rmtree(DIR_REPO)

    os.mkdir(DIR_REPO)
    os.system(
        '; '.join([
            f'cd {DIR_ROOT}',
            f'git clone {GIT_REPO_URL}',
            'cd news_lk2',
            'git checkout data',
        ])
    )
    log.debug(f'Cloned {GIT_REPO_URL} [data] to {DIR_REPO}')


def get_date_ids():
    dir_article_root = get_dir_article_root()
    return list(filter(
        lambda file_name: len(file_name) == 8 and file_name[:4] != '.git',
        os.listdir(dir_article_root),
    ))


def get_newspapers_for_date(date_id):
    dir_date = get_dir_date(date_id)
    return list(filter(
        lambda file_name: file_name not in IGNORE_LIST,
        os.listdir(dir_date),
    ))


def get_article_files_for_date_and_newspaper(date_id, newspaper_id):
    dir_date_and_newspaper = get_dir_date_and_newspaper(
        date_id, newspaper_id)
    article_files_only = list(filter(
        lambda file_name: len(file_name) == 13 and file_name[-5:] == '.json',
        os.listdir(dir_date_and_newspaper),
    ))
    return list(map(
        lambda article_file_only: os.path.join(
            dir_date_and_newspaper,
            article_file_only,
        ),
        article_files_only,
    ))
