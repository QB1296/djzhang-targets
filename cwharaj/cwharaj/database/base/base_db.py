import pymongo


class BaseDatabase(object):
    def __init__(self, host, port, user, passwd, db, collection_name):
        pass

    def open_spider(self):
        pass

    def close_spider(self):
        pass

    def insert_for_cache(self, item):
        pass

    def insert_for_history(self, item):
        pass

    def insert_for_item(self, item):
        pass

    def update_for_history(self, id, item):
        pass

    def get_count(self, dict):
        pass

    def delete_row(self, _last, url_from):
        pass

    def find_oldest_for_cache(self):
        pass

    def check_exist_by_id(self, _id):
        return False