# -*- coding: utf-8 -*-

import scrapy
from scrapy.selector import Selector


class PoliticlsWatchSpider(scrapy.Spider):
    name = "politicl_watch"
    allowed_domains = [
        "www.dnaindia.com",
        "www.indianexpress.com",
        "http://theviewspaper.net"
    ]
    start_urls = [
        'http://www.dnaindia.com/analysis',
        'http://indianexpress.com/opinion/',
        'http://theviewspaper.net',
    ]

    def __init__(self, name=None, **kwargs):
        from cwpoliticl.database_factory import DatabaseFactory, CollectionTypes
        database_factory = DatabaseFactory(kwargs['host'], kwargs['port'],
                                           kwargs['user'], kwargs['passwd'],
                                           kwargs['db'], kwargs['collection_name'])

        self._cache_db = database_factory.get_database(CollectionTypes.cache)
        self._history_db = database_factory.get_database(CollectionTypes.history)

        from cwpoliticl.extensions.dnaindia_parser import DnaIndiaParser
        self._dna_india_Parse = DnaIndiaParser()

        from cwpoliticl.extensions.indianexpress_parser import IndianExpressParser
        self._indian_express_Parse = IndianExpressParser()

        from cwpoliticl.extensions.theviewspaper_parser import TheViewsPaperParser
        self._the_views_paper_Parse = TheViewsPaperParser()

        super(PoliticlsWatchSpider, self).__init__(name, **kwargs)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return super(PoliticlsWatchSpider, cls).from_crawler(crawler,
                                                             args,
                                                             host=crawler.settings.get('SQL_HOST'),
                                                             port=crawler.settings.get('SQL_PORT'),
                                                             user=crawler.settings.get('SQL_USER'),
                                                             passwd=crawler.settings.get('SQL_PASSWD'),
                                                             db=crawler.settings.get('SQL_DB'),
                                                             collection_name=crawler.settings.get(
                                                                 'SQL_COLLECTION_NAME')
                                                             )

    def parse(self, response):
        self._crawl_parser.parse_paginate(response.url, response, self._cache_db, self._history_db)

    def parse_detail(self, response):
        item = self._crawl_parser.parse(response.url, response)
        yield item

        yield scrapy.Request(item['cluster'], self.parse_cluster)

        # yield scrapy.Request(response.url, self.parse_relatived_app)

        # the below is that crawl a random relatived app.
        select = '//a[@class="card-click-target"]'
        sel = Selector(response)
        navs = sel.xpath(select)

        if not self._history_db.check_exist(abstractPath):
            yield scrapy.Request(abstractPath, self.parse_detail, meta={'type': title})
