# -*- coding: utf-8 -*-

import warnings
import unittest
import time

from cwharaj.utils.crawl_utils import CrawlUtils
from cwharaj.items import CacheItem, HistoryItem
from datetime import datetime


class MysqlDBTest(unittest.TestCase):
    def setUp(self):
        from cwharaj.database.base.mysql_db import MysqlDatabase

        # db_type = ''
        db_type = '_history'
        # db_type = '_cache'

        self.mysql_database = MysqlDatabase(
            host='localhost',
            port=3306,
            user='haraj', passwd='haraj720',
            db="vps_scrapy_rails",
            collection_name="haraj{}".format(db_type))

    # def test_insert_cache_item(self):
    #     _url = "https://sa.opensooq.com/ar/search/30002057/استراحة-سديم-للايجار-اليومي-والشهري-والسنوي-حي-الأمانة-شمال-الرياض"
    #     _guid = "1234321"
    #     # _id = CrawlUtils.url_parse_id_from_page_url(_url, 3)
    #     _id = "123"
    # 
    #     self.mysql_database.open_spider()
    #     item = CacheItem(
    #         url=_url,
    #         guid=_guid,
    #         created_at=datetime.utcnow().replace(microsecond=0).isoformat(' '),
    #         ID=_id,
    #         url_from="opensooq"
    #     )
    #     self.mysql_database.insert_for_cache(item)


    def test_insert_history_item(self):
        _url = "https://sa.opensooq.com/ar/search/30002057/استراحة-سديم-للايجار-اليومي-والشهري-والسنوي-حي-الأمانة-شمال-الرياض"
        _guid = "1234321"
        # _id = CrawlUtils.url_parse_id_from_page_url(_url, 3)
        _id = "123"

        self.mysql_database.open_spider()
        item = HistoryItem(
            url=_url,
            guid=_guid,
            created_at=datetime.utcnow().replace(microsecond=0).isoformat(' '),
            ID=_id
        )
        self.mysql_database.insert_for_history(item)
