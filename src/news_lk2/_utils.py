"""Utils."""
import time

from utils import logx

log = logx.get_logger('news_lk2')

TIMEZONE_SRI_LANKA = 19800


def get_seconds_behind_sl():
    return time.timezone + TIMEZONE_SRI_LANKA
