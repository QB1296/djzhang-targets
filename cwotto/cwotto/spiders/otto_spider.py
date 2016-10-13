# -*- coding: utf-8 -*-
from random import Random

import scrapy
from cwotto.items import Product


class OttoSpider(scrapy.Spider):
    name = "otto"
    allowed_domains = ["oto.com"]
    start_urls = [
        # 'https://www.otto.de/p/bruno-banani-blazer-im-uniform-look-512770595#variationId=512770596',
        'https://www.otto.de/p/sit-sideboard-corsica-breite-150-cm-562203065#variationId=562204027',
        # "https://www.otto.de/p/melrose-blazer-509995713/#variationId=509998431"
    ]

    def __init__(self, name=None, **kwargs):
        from cwotto.parser.response_parser import ResponseParse
        self._crawl_parser = ResponseParse()

        super(OttoSpider, self).__init__(name, **kwargs)

    def parse(self, response):
        url = response.request.url
        split = url.split("#")
        if len(split) == 2:
            para = split[1]
            s = para.split('=')
            if len(s) == 2:
                variationId = s[1]

                item = self._crawl_parser.parse_item(url, response, variationId)
                yield item
