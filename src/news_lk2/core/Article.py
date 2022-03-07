import os

from utils import hashx, jsonx, timex

from news_lk2._utils import log

SALT = '5568445278803347'
HASH_LENGTH = 8


class Article:
    def __init__(self, newspaper_name, url, time_ut, title, body_lines):
        self.newspaper_name = newspaper_name
        self.url = url
        self.time_ut = time_ut
        self.title = title
        self.body_lines = body_lines

    @property
    def file_name(self):
        date_id = timex.get_date_id(self.time_ut)
        dir = f'/tmp/news_lk2/{date_id}/{self.newspaper_name}'
        if not os.path.exists(dir):
            os.system(f'mkdir -p {dir}')
        h = hashx.md5(self.url + SALT)[:HASH_LENGTH]
        return os.path.join(dir, f'{h}.json')

    @property
    def dict(self):
        return dict(
            newspaper_name=self.newspaper_name,
            url=self.url,
            time_ut=self.time_ut,
            title=self.title,
            body_lines=self.body_lines,
        )

    def store(self):
        jsonx.write(self.file_name, self.dict)
        log.info(f'Wrote {self.file_name}')
