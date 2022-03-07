
from bs4 import BeautifulSoup
from utils import timex, www

from news_lk2._utils import log
from news_lk2.core import Article

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
    title = h1_title.text.strip()
    body_lines = list(map(
        lambda line: line.strip(),
        header_inner.text.strip().split('\n'),
    ))
    article = Article(
        newspaper_name=NEWSPAPER_NAME,
        url=url,
        time_ut=time_ut,
        title=title,
        body_lines=body_lines,
    )
    article.store()


def scrape():
    log.debug(f'Scraping {URL_NEWS}')
    html = www.read(URL_NEWS)
    soup = BeautifulSoup(html, 'html.parser')

    n_articles = 0
    for div in soup.find_all('div', {'class': 'col-md-8'}):
        article_url = div.find('a').get('href')
        scrape_and_save_article(article_url)
        n_articles += 1
    log.info(f'Scraped {n_articles} off {URL_NEWS}')
