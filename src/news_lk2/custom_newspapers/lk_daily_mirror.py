import os

from bs4 import BeautifulSoup
from utils import jsonx, www

from news_lk2._utils import log

URL_NEWS = 'https://www.dailymirror.lk/news/209'
DIR_OUTPUT = '/tmp/news_lk2'


def init():
    if not os.path.exists(DIR_OUTPUT):
        os.mkdir(DIR_OUTPUT)


def scrape_article(url):
    log.info(f'Scraping article {url}')
    html = www.read(url)
    soup = BeautifulSoup(html, 'html.parser')
    h1_title = soup.find('h1')
    span_time = soup.find('span', {'class': 'gtime'})
    header_inner = soup.find('header', {'class': 'inner-content'})

    return {
        'url': url,
        'title': h1_title.text.strip(),
        'time_raw': span_time.text.strip(),
        'body_lines': list(map(
            lambda line: line.strip(),
            header_inner.text.strip().split('\n'),
        )),
    }


def scrape_index(index_url):
    log.info(f'Scraping index {index_url}')
    html = www.read(index_url)
    soup = BeautifulSoup(html, 'html.parser')

    article_list = []
    for div in soup.find_all('div', {'class': 'col-md-8'}):
        article_url = div.find('a').get('href')
        article = scrape_article(article_url)
        article_list.append(article)
        break

    article_list_file = '/tmp/news_lk2/article_list.json'
    jsonx.write(article_list_file, article_list)
    log.info(f'Wrote {article_list_file}')


if __name__ == '__main__':
    init()
    scrape_index(URL_NEWS)
