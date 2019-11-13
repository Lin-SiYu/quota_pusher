import motor
from tornado.options import options

from lib.log import logger_error


class MongodbHandler(object):
    def __init__(self, uri=None, db=None):
        try:
            if not uri:
                uri = options['MONGO_URI']
            self.client = motor.motor_tornado.MotorClient(uri)
            if not db:
                db = options['MONGO_DB']
            self.db = self.client[db]
        except AttributeError as e:
            logger_error.error('AttributeError - %s' % e)

    def get_conn(self):
        return self.client

    def get_db(self):
        return self.db

    async def do_find_one(self, doc_name, filter=None, *args, **kwargs):
        return await self.db[doc_name].find_one(filter, *args, **kwargs)

    async def do_find(self, doc_name, filter=None, *args, **kwargs):
        cursor = self.db[doc_name].find(filter, *args, **kwargs)
        doc_list = []
        async for document in cursor:
            doc_list.append(document)
        return doc_list

    async def do_insert_one(self, doc_name, document, **kwargs):
        # document = {"name": "hello", "age": "19"}
        return await self.db[doc_name].insert_one(document, **kwargs)

    async def do_insert_many(self, doc_name, document, **kwargs):
        # document = [{},{}]
        return await self.db[doc_name].insert_many(document, **kwargs)
