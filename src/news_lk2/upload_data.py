from news_lk2.analysis import paper
from news_lk2.custom_newspapers import DailyMirrorLk

if __name__ == '__main__':
    DailyMirrorLk().scrape()
    paper.run_daily_job()
