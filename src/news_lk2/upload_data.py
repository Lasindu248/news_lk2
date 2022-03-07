from news_lk2.analysis import paper
from news_lk2.custom_newspapers import DailyFtLk, DailyMirrorLk

if __name__ == '__main__':
    DailyMirrorLk().scrape()
    DailyFtLk().scrape()
    paper.run_daily_job()
