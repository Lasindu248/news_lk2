import os

from utils import hashx, timex

SALT = '5568445278803347'
HASH_LENGTH = 8


def get_article_file(newspaper_name, time_ut, url):

    date_id = timex.get_date_id(time_ut)
    dir = f'/tmp/news_lk2/{date_id}/{newspaper_name}'
    if not os.path.exists(dir):
        os.system(f'mkdir -p {dir}')
    h = hashx.md5(url + SALT)[:HASH_LENGTH]
    return os.path.join(dir, f'{h}.json')
