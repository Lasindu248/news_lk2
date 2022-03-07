
from bs4 import BeautifulSoup
from utils import jsonx, timex, www

from news_lk2._utils import log
from news_lk2.core.article import get_article_file
from news_lk2.core.common import init

URL_NEWS = 'https://www.dailymirror.lk/latest-news/342'
TIME_RAW_FORMAT = '%d %B %Y %I:%M %p'
TIME_FORMAT = '%Y-%m-%d %H:%M'
NEWSPAPER_NAME = 'lk_daily_mirror'


def parse_time(time_raw):
    return timex.parse_time(time_raw, TIME_RAW_FORMAT)


def scrape_and_save_article(url):
    log.debug(f'Scraping article {url}')
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')
    h1_title = soup.find('h1')
    span_time = soup.find('span', {'class': 'gtime'})
    header_inner = soup.find('header', {'class': 'inner-content'})

    time_ut = parse_time(span_time.text.strip())
    time_str = timex.format_time(time_ut, TIME_FORMAT)
    article = {
        'url': url,
        'title': h1_title.text.strip(),
        'time_ut': time_ut,
        'time_str': time_str,
        'body_lines': list(map(
            lambda line: line.strip(),
            header_inner.text.strip().split('\n'),
        )),
    }
    article_file = get_article_file(NEWSPAPER_NAME, article['time_ut'], url)
    jsonx.write(article_file, article)
    log.info(f'Wrote {article_file}')


def scrape_index(index_url):
    log.info(f'Scraping index {index_url}')
    html = www.read(index_url)
    soup = BeautifulSoup(html, 'html.parser')

    for div in soup.find_all('div', {'class': 'col-md-8'}):
        article_url = div.find('a').get('href')
        scrape_and_save_article(article_url)


if __name__ == '__main__':
    init()
    scrape_index(URL_NEWS)
