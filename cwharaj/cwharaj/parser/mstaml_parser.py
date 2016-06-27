import logging

from cwharaj.items import Ad, CacheItem, WebsiteTypes, City, Member
from cwharaj.parser.base_parser import BaseParser
from cwharaj.parser.utils.harajs_comments import HarajsComments
from cwharaj.parser.utils.harajs_section import HarajsSection


class MstamlParse(BaseParser):
    def __init__(self):
        super(MstamlParse, self).__init__()

    # Here,we store items from newest to oldest.
    # then fetch the first item from the databse become the oldest.
    def parse_paginate(self, url, hxs, cache_db, history_db):
        links = hxs.xpath('//*[@class="center mb10 "]/div')
        logging.debug("Get rows count from the mstaml: {}.".format(len(links)))

        count = 1
        for link in links:
            Li_selector = '//*[@class="center mb10 "]/div[' + str(count) + ']'
            div_class_selector = '//*[@class="center mb10 "]/div[' + str(count) + ']/@class'

            count += 1

            class_name = self.get_value_response(hxs, div_class_selector)
            # This div is empty line, such as "<div id="item2072286" class="none"></div>"
            # This div is empty line, such as "<div id="item2072286" class="clear"></div>"
            # valid div is "class="boxDarkBody dw1 gWhite ui-corner-all mb20 mt20""
            if len(class_name) <= 10:
                logging.debug("ignore the empty line, class name: {}, at {}".format(class_name, count - 1))
                continue

            href = self.get_value_response(hxs, Li_selector + '/*[@class="pb3"]/a[@class="xRight fL1"]/@href')

            from cwharaj.utils.crawl_utils import CrawlUtils
            _ID = CrawlUtils.url_parse_id_from_page_url(href, 1)

            # If the link already exist on the history database,ignore it.
            if history_db.check_exist_by_id(_ID):
                logging.debug("  item exist {} on the history database".format(_ID))
                continue

            item = CacheItem(
                ID=_ID,
                url_from=WebsiteTypes.mstaml.value,
            )

            cache_db.process_item(href, item, count)
            # here, must sleep a second.
            # time.sleep(1)

    def parse(self, url, hxs, item_db, phoneNumberSet=None):
        from cwharaj.utils.crawl_utils import CrawlUtils
        _ID = CrawlUtils.url_parse_id_from_page_url(url, 1)

        # boxItem
        _time = self.get_value_response(hxs, '//*[@class="boxItem"]/table[1]/tr/td[2]/span/text()')

        # AD
        _ads_title = self.get_value_response(hxs, '//*[@class="titleSection doHighlight"]/text()')
        _image_link = self.get_images_in_selector(hxs, '//noscript')
        _ads_body = self.get_all_value_response(hxs,
                                                '//*[@class="text linkify linkifyWithImages linkifyWithWasel doHighlight"]/text()')

        # Member
        _number = self.get_value_response(hxs, '//table[@class="dcs"]/tbody/tr[9]/td[2]/text()')

        _ads_city = self.get_value_response(hxs,
                                            '//*[@class="boxDarkBody p1"]/table/tr[2]/td[@class="gH3 xCenter p3 fB"]/text()')
        _memberName = self.get_value_response(hxs, '//*[@class="boxItem"]/table[1]/tr/td[1]/b/text()')

        # Sections
        _sections = self.get_section(hxs, '//div[@class="pageRight"]/h1[@class="titlePage"]/a/text()')
        _section_item = HarajsSection(_sections, item_db).get_section_item()

        # Replace "\n","\r"
        _ads_city = _ads_city.replace("\n", "").replace("\r", "").strip()

        # ====
        # Save to relative database
        # ====
        _city_id = item_db.save_city(City.get_default(_ads_city))

        _His_announcement_id = item_db.save_member(Member.get_default(_memberName))

        item = Ad.get_default(
            section_item=_section_item,
            _ads_title=_ads_title,
            _city_id=_city_id,
            _ads_contact=_ads_contact,
            _ads_body=_ads_body,
            _image_link=_image_link,
            _His_announcement_id=_His_announcement_id,
            _type_ads_or=1, _close_ads=0
        )

        id_ads = item_db.save_ad(item)

        return item

    def get_section(self, hxs, selector):
        _As = hxs.xpath(selector).extract()

        sections = []
        for a in _As:
            sections.append(a.encode('utf-8'))

        return ",".join(sections)
