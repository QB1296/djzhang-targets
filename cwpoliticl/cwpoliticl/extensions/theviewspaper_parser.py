import urlparse

from cwpoliticl.extensions.base_parser import BaseParser
from cwpoliticl.extensions.rpc.wordpress_xml_rpc_utils import WDXmlRPCUtils
from cwpoliticl.items import CacheItem, WebsiteTypes, WDPost


class TheViewsPaperParser(BaseParser):
    def __init__(self):
        self._url_from = WebsiteTypes.theviewspaper.value
        super(TheViewsPaperParser, self).__init__()

    def parse_paginate(self, url, hxs, cache_db, history_db):
        selector = '//*[@class="container"]/*[@class="row"]/*[@class="col-md-8"]/article/a/@href'
        links = hxs.xpath(selector).extract()  # Type: List['unicode']

        for href in links:
            # If the link already exist on the history database, ignore it.
            if history_db.check_history_exist(href):
                continue

            cache_db.save_cache(CacheItem.get_default(url=href, url_from=self._url_from))

    def parse(self, url, hxs, wd_rpc):
        title = self.get_value_response(hxs, '//*[@class="heading-part"]/*[@itemprop="headline"]/text()')
        image = self.get_value_response(hxs, '//*[@itemprop="articleBody"]/*[@class="custom-caption"]/img/@src')
        content = self.get_all_value_response(hxs, '//*[@itemprop="articleBody"]/p', max_len=2, sperator='\n' + '\n')

        tags = hxs.xpath('//*[@class="storytags"]/ul/li/a/text()').extract()

        item = WDPost(url=url, url_from=self._url_from, title=title, image=image, content=content, tags=tags)

        post_id = wd_rpc.post_to_wd(item)

        pass
