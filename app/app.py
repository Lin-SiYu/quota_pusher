import asyncio

from tornado.web import Application

from lib.db.db_utils import MysqlPool
from lib.loggers import log_function
from lib.mongo.mongo_base import MongodbHandler
from lib.rabbit_mq.mq_base import MqBase
from lib.redis.redis_utils import RedisPool
from .routers import BaseRoutingHandler
from tornado_swagger.setup import setup_swagger


def make_app(cookie_secret, debug):
    base_routing = BaseRoutingHandler()
    mongo = MongodbHandler()

    settings = dict(
        login_url='/login',
        cookie_secret=cookie_secret,
        log_function=log_function,
        debug=debug,
        mongo=mongo,
    )
    _handlers = base_routing.interface_map_list

    setup_swagger(_handlers, title='quota-pusher')
    app = Application(
        handlers=_handlers, **settings)

    app.db = MysqlPool().get_manager()
    app.redis = asyncio.get_event_loop().run_until_complete(RedisPool.create()).get_conn()
    app.mq = MqBase()
    return app
