import datetime

from ioc_fetch.app import db
from tests import AppTest


class APITest(AppTest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def strp_strf(self, dt_str):
        fmt = '%Y-%m-%dT%H:%M:%S.%f+00:00'
        return datetime.datetime.strptime(dt_str, fmt).strftime(fmt)
