from cwpoliticl.extensions.base_parser import BaseParser
from cwpoliticl.items import CacheItem, WDPost


class DnaIndiaParser(BaseParser):
    page_selector_dict = {
        "title": '//*[@class="img-caption"]/h1/text()',
        "image": '//*[@class="row article-img pos-lead"]/img/@src',
        "content": '//*[@class="body-text"]/p/text()',
        "tags": '//*[@data-event-sub-cat="ArticleTags"]/div/div/ul/li/a/text()',
    }

    def __init__(self):
        from cwpoliticl.scraped_websites import WebsiteTypes
        self.url_from = WebsiteTypes.dnaindia.value
        super(DnaIndiaParser, self).__init__()

    def parse_paginate(self, url, hxs, cache_db, history_db):
        select_block = '//*[@class="media-list eventtracker"]'
        self._parse_block_for_pagination(url, hxs, cache_db, history_db, select_block)

    def _parse_block_for_pagination(self, url, hxs, cache_db, history_db, select_block):
        links = hxs.xpath(select_block).extract()

        for idx, link in enumerate(links):
            href_selector = '{}/div[{}]/div[@class="media-left"]/a/@href'.format(select_block, (idx + 1))
            thumbnail_selector = '{}/div[{}]/div[@class="media-left"]/a/img/@src'.format(select_block, (idx + 1))

            href = self.get_value_with_urljoin(hxs, href_selector, url)
            if history_db.check_history_exist(href):  # If the link already exist on the history database, ignore it.
                continue

            thumbnail_src = self.get_value_response(hxs, thumbnail_selector)
            cache_db.save_cache(CacheItem.get_default(url=href, thumbnail_url=thumbnail_src, url_from=self.url_from))

    def parse(self, url, hxs, wd_rpc, thumbnail_url, access_denied_cookie=None):
        title = self.get_value_response(hxs, self.page_selector_dict['title'])
        image_src = self.get_value_response(hxs, self.page_selector_dict['image'])
        content = self.get_all_value_response(hxs, self.page_selector_dict['content'])
        tags = hxs.xpath(self.page_selector_dict['tags']).extract()

        item = WDPost.get_default(url, self.url_from, title, image_src, thumbnail_url, content, tags)

        post_id = wd_rpc.post_to_wd(item)

        return item
