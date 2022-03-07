from news_lk2.analysis import paper
from news_lk2.custom_newspapers import DailyMirrorLK

if __name__ == '__main__':
    DailyMirrorLK().scrape()
    paper.run_daily_job()
