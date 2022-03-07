from news_lk2.core.common import init
from news_lk2.custom_newspapers import lk_daily_mirror

if __name__ == '__main__':
    init()
    lk_daily_mirror.scrape()
