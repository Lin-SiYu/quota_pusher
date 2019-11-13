from tornado import gen
from tornado.web import HTTPError

from app.errors import HTTPAPIError
from app.models.test_model import TestModel
from lib.base import APIHandler
from lib.jwt_utils.jwt_decorators import jwt_required
from lib.log import logger_info


# noinspection PyAbstractClass
class MainHandler(APIHandler):
    def get(self):
        # logger_info.info(5 / 0)
        raise HTTPError(401)


class SecondHandler(APIHandler):

    @jwt_required
    async def get(self):
        a = await self.aa()
        # self.write({'result': a})
        raise HTTPAPIError(10011)

    async def aa(self):
        return 1
        # raise gen.Return(self.success_json('1', '2', '3'))


class RedisHandler(APIHandler):
    async def get(self):
        val = await self.redis.set('xxx', 123)

        self.write(self.success_json(val))


class MysqlHandler(APIHandler):
    async def get(self):
        all_objects = await self.db.execute(TestModel.select())
        for obj in all_objects:
            self.write(self.success_json(obj.text))


class MongoAPIHandler(APIHandler):
    @gen.coroutine
    def get(self):
        mongo = self.settings['mongo']
        res = yield mongo.do_find_one('testtable', {'name': 'name'})
        logger_info.info(res)
        # print(res)
        r = yield mongo.do_find('testtable', limit=3)
        # print(r)
        self.write('ok')
