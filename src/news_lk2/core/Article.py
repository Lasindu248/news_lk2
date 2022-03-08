import math

from utils import jsonx, timex

from news_lk2._utils import log
from news_lk2.core.filesys import get_article_file

WORDS_PER_MINUTE = 250


class Article:
    def __init__(self, newspaper_id, url, time_ut, title, body_lines):
        self.newspaper_id = newspaper_id
        self.url = url
        self.time_ut = time_ut
        self.title = title
        self.body_lines = body_lines

    @property
    def file_name(self):
        return get_article_file(
            self.time_ut,
            self.newspaper_id,
            self.url,
        )

    @property
    def time_short_str(self):
        return timex.format_time(self.time_ut, '%I:%M%p, %B %d')

    @property
    def url_domain(self):
        tokens = self.url.split('/')
        return tokens[2].replace('www.', '')

    @property
    def word_count(self):
        text = self.title + ' ' + ' '.join(self.body_lines)
        words = text.split(' ')
        return len(words)

    @property
    def reading_time_min(self):
        return math.ceil(self.word_count / WORDS_PER_MINUTE)

    @property
    def dict(self):
        return dict(
            newspaper_id=self.newspaper_id,
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
            newspaper_id=d['newspaper_id'],
            url=d['url'],
            time_ut=d['time_ut'],
            title=d['title'],
            body_lines=d['body_lines'],
        )
