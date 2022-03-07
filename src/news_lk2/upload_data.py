from news_lk2.analysis import paper
from news_lk2.custom_newspapers import lk_daily_mirror

if __name__ == '__main__':
    lk_daily_mirror.scrape()
    paper.run_daily_job()
