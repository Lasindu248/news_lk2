
from utils import jsonx, timex

from news_lk2._utils import log
from news_lk2.core.filesys import get_article_file


class Article:
    def __init__(self, newspaper_name, url, time_ut, title, body_lines):
        self.newspaper_name = newspaper_name
        self.url = url
        self.time_ut = time_ut
        self.title = title
        self.body_lines = body_lines

    @property
    def file_name(self):
        return get_article_file(
            self.time_ut,
            self.newspaper_name,
            self.url,
        )
    @property
    def time_only_str(self):
        return timex.format_time(self.time_ut, '%H:%M')

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

    def __lt__(self, other):
        return self.time_ut < other.time_ut

    @staticmethod
    def load(article_file):
        d = jsonx.read(article_file)
        return Article(
            newspaper_name=d['newspaper_name'],
            url=d['url'],
            time_ut=d['time_ut'],
            title=d['title'],
            body_lines=d['body_lines'],
        )
