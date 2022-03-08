from news_lk2.core.filesys import git_checkout
from news_lk2.custom_newspapers import newspaper_class_list

if __name__ == '__main__':
    git_checkout()
    for newspaper_class in newspaper_class_list:
        newspaper_class.scrape()
