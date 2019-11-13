from app.mq_register.market_pair import pairs_get, pairs_register, market_pair_publish
from lib.middleware.example_middle import ExampleMiddleware
from lib.rabbit_mq.consumer import consumer
from lib.rabbit_mq.heartbeat_consumer import heartbeat_example


async def register(app):
    '''
    根据业务逻辑，注册需要初始化队列的对象信息
    ！注意！：需保证exchange存在
    '''
    # 提供 Asynchronous callback，自定义queue_name,已存在的exchange_name
    # await consumer.register(heartbeat_example, 'heartbeat_test', 'Heartbeat')
    # await consumer.register(ExampleMiddleware().publish, 'example_middle', 'Example')

    # 下列为测试简写
    # pairs = {'BTC': ['BTC/USDT', ], 'ETH': ['ETH/USDT', ], }
    # PAIRS DATA FROM MYSQL
    pairs = await pairs_get(app)
    for symbol, coin_pairs in pairs.items():
        await pairs_register(market_pair_publish, symbol, coin_pairs)
