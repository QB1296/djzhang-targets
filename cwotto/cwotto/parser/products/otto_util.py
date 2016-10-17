from cwotto.parser.base_parser import BaseParser


class OttoUtil(object):
    def __init__(self, hxs, url, product_json, variationId):
        self.hxs = hxs
        self.url = url
        self.product_json = product_json
        self.variationId = variationId
        super(OttoUtil, self).__init__()

    def get_product_description(self):
        return BaseParser.extract_by_query(self.hxs, '//*[@class="article-properties-body"]')

    def get_title(self):
        __variation = self.product_json["variations"][self.variationId]
        _title = __variation['name']
        return _title