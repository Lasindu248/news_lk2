from news_lk2.analysis import paper
from news_lk2.custom_newspapers import newspaper_class_list

if __name__ == '__main__':
    for newspaper_class in newspaper_class_list:
        newspaper_class().scrape()
    paper.run_daily_job()
