import math

from utils import jsonx, timex

from news_lk2._constants import WORDS_PER_MINUTE
from news_lk2._utils import log
from news_lk2.core.filesys import get_article_file, get_hash

MINUTES_PER_TRUNCATED_BODY = 1
MAX_WORDS_TRUNCATED = WORDS_PER_MINUTE * MINUTES_PER_TRUNCATED_BODY


class Article:
    def __init__(self, newspaper_id, url, time_ut, title, body_lines):
        self.newspaper_id = newspaper_id
        self.url = url
        self.time_ut = time_ut
        self.title = title
        self.body_lines = body_lines

    @property
    def url_hash(self):
        return get_hash(self.url)

    @property
    def file_name(self):
        return get_article_file(self.url)

    @property
    def date_id(self):
        return timex.get_date_id(self.time_ut, timex.TIMEZONE_OFFSET_LK)

    @property
    def time_short_str(self):
        return timex.format_time(
            self.time_ut,
            '%I:%M%p, %A, %B %d, %Y',
            timex.TIMEZONE_OFFSET_LK,
        )

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

    @property
    def body_lines_truncated(self):
        truncated_body_lines = []
        word_count = 0
        for line in self.body_lines:
            truncated_body_lines.append(line)

            words = line.split(' ')
            word_count += len(words)
            if word_count > MAX_WORDS_TRUNCATED:
                return truncated_body_lines + ['...']

        return self.body_lines
