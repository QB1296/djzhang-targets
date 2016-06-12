import MySQLdb
from cwharaj.database.base.base_db import BaseDatabase
import logging


class MysqlDatabase(BaseDatabase):
    def __init__(self, host, port, user, passwd, db, collection_name):
        super(MysqlDatabase, self).__init__(host, port, user, passwd, db, collection_name)
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.collection_name = collection_name

    def connect(self):
        try:
            self.client = MySQLdb.Connection(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                port=self.port
            )
        except (AttributeError, MySQLdb.OperationalError), e:
            raise e

    def open_spider(self):
        self.connect()
        # prepare a cursor object using cursor() method
        self.cursor = self.client.cursor()

    def close_spider(self):
        # disconnect from server
        self.client.close()

    def insert_for_cache(self, item):

        sql = """ INSERT INTO {} (url, guid, created_at, ID, url_from) VALUES ('{}','{}','{}','{}','{}')""".format(
            self.collection_name, item['url'], item['guid'], item['created_at'], item['ID'], item['url_from'])

        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.client.commit()
        except Exception, e:
            logging.debug("  mysql: insert the cache item failure, {}".format(e.message))
            # Rollback in case there is any error
            self.client.rollback()

        logging.debug("  mysql: insert {} into the {} successfully".format(item['ID'], self.collection_name))

    def insert_for_item(self, item):
        self.collection.insert(dict(item))

    def insert_for_history(self, item):
        sql = """ INSERT INTO {} (url, guid, created_at, ID) VALUES ('{}','{}','{}','{}')""".format(
            self.collection_name, item['url'], item['guid'], item['created_at'], item['ID'])

        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.client.commit()
        except Exception, e:
            logging.debug("  mysql: insert the cache item failure, {}".format(e.message))
            # Rollback in case there is any error
            self.client.rollback()

        logging.debug("  mysql: insert {} into the {} successfully".format(item['ID'], self.collection_name))

    def update_for_history(self, id, item):
        if not self.check_exist_by_id(id):
            self.insert_for_history(item)

    def get_count(self, dict):
        count = self.collection.count(dict)
        return count

    def delete_row(self, _last, url_from):
        # 1. Parse the url and get the unique id.
        from cwharaj.items import WebsiteTypes
        _position = WebsiteTypes.get_id_index(url_from)

        from cwharaj.utils.crawl_utils import CrawlUtils
        _id = CrawlUtils.url_parse_id_from_page_url(_last, _position)
        logging.debug("  2. get the last url's id: {}".format(_id))

        # Generate a query dictionary.
        deleted_dict = {'ID': _id}

        # Query the deleted item count, must be equal to 1.
        # count = self.collection.count(deleted_dict)
        count = self.get_count(deleted_dict)
        logging.debug("  3. found the deleted item count: {} by ID".format(count, deleted_dict))
        if count:
            result = self.collection.delete_one(deleted_dict)
            logging.debug(
                "  4. deleted cache row, id: {}, deleted count: {}, from {}"
                    .format(_id, result.deleted_count, url_from))

    def find_oldest_for_cache(self):
        """Query the oldest cache item."""

        cursor = self.collection.find().sort([("created_at", pymongo.ASCENDING)])
        logging.debug("  5. current cache items count: {}".format(cursor.count()))

        row = None
        if cursor.count():
            row = cursor.next()
            logging.debug("  6. found the oldest row sucessfully, ID: {}".format(row['ID']))

        cursor.close()

        return row

    def check_exist_by_id(self, _id):
        sql = """ SELECT 1 FROM {} WHERE ID = {}""".format(self.collection_name, _id)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
        except Exception, e:
            logging.debug("  mysql: check {} exist from {} failure, {}".format(_id, self.collection_name, e.message))
            return False

        ret = self.client.fetchone()[0]
        if ret:
            return True

        return False
