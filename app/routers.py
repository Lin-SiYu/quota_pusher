from app.handlers.mq_handlers import MQProducerHander, MQConsumerHander
from app.handlers.ws_handlers.market_pair_handler import MarketPairHandler
from app.handlers.ws_handlers.ws_handlers import ExampleHandler
from .handlers import MainHandler, SecondHandler, RedisHandler, MysqlHandler, MongoAPIHandler
import tornado.web


class BaseRoutingHandler(object):
    def __init__(self):
        self.interface_map_list = []
        self.router_register()

    def router_register(self):
        router_list = [
            (r'/v1/hello', MainHandler),
            (r'/v1/hello02', SecondHandler),
            (r'/v1/mongo', MongoAPIHandler),
            (r'/v1/redis', RedisHandler),
            (r'/v1/mysql', MysqlHandler),
            (r'/v1/mq/producer', MQProducerHander),
            (r'/v1/mq/consumer', MQConsumerHander),

            (r'/v1/ws/example', ExampleHandler),
            (r'/v1/ws/marketpair', MarketPairHandler),

        ]
        # self.interface_map_list.extend(router_list)
        self.interface_map_list.extend(map(lambda x: tornado.web.url(*x), router_list))
