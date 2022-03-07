import os

DIR_OUTPUT = '/tmp/news_lk2'


def init():
    if not os.path.exists(DIR_OUTPUT):
        os.mkdir(DIR_OUTPUT)
