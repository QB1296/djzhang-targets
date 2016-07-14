from cwharaj.items import WebsiteTypes

from cwharaj.parser.opensooq_parser import OpensooqParse
from cwharaj.parser.mstaml_parser import MstamlParse
from cwharaj.parser.harajsa_parser import HarajSaParse


class BaseDispatch(object):
    def __init__(self):
        self.allowed_domains = [
            "https://sa.opensooq.com/",
            'http://www.mstaml.com',
            'https://haraj.com.sa',
        ]
        self.websites = {
            'https://sa.opensooq.com': WebsiteTypes.opensooq,
            'http://www.mstaml.com': WebsiteTypes.mstaml,
            'https://haraj.com.sa': WebsiteTypes.harajsa,
        }

        self.parses = {
            WebsiteTypes.opensooq: OpensooqParse(),
            WebsiteTypes.mstaml: MstamlParse(),
            WebsiteTypes.harajsa: HarajSaParse()
        }
        super(BaseDispatch, self).__init__()

    def get_allowed_domains(self):
        return self.allowed_domains

    def get_pagination_websites(self):
        return self.websites.keys()

    def parse_from_pagination(self, url, hxs, cache_db, history_db):
        type = self.websites[url]
        parse = self.parses[type]

        parse.parse_paginate(url, hxs, cache_db, history_db)
