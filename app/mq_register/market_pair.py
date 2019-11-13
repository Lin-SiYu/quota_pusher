import gzip
import json

import peewee_async

from lib.rabbit_mq.consumer import consumer
from lib.middleware import WS_CONNECT_USER_INFOS as user_infos


async def pairs_get(app):
    '''
    获取 mongodb - thetoken_test 中 币对collection-name 作为 MQ 队列名
    :param app:
    :return: 币对字典 {'BTC': ['BTC/USDT', ], 'ETH': ['ETH/USDT', ], }
    '''
    query_sql = 'SELECT pair_name FROM `transaction_pair_new` GROUP BY `pair_name`;'
    # aiomysql.cursors.Cursor
    cursor = await peewee_async._run_sql(app.db.database, query_sql)
    res = await cursor.fetchall()
    await cursor.close()
    name_list = [r[0] for r in res]

    pairs_dic = {}
    for name in name_list:
        if name.isupper():
            # 若大写，证明为币对
            currency = name.split('/')[0]
            if currency not in pairs_dic:
                pairs_dic[currency] = []
            pairs_dic[currency].append(name)
    return pairs_dic


async def pairs_register(callback, symbol, pairs_list, exchange='MarketPair', multi=False):
    '''
    初始化，币对相关的注册
    :param callback: Asynchronous callback
    :param symbol: 币种，例如：BTC
    :param pairs_list: 币对列表，e.g. ['BTC/USDT','BTC/CNY' ]
    :param exchange: 绑定交换机名，必须确保存在,默认为'MarketPair'；注意！该业务逻辑下，必须为topic类型
    :param mutil: 是否批量匹配，默认不批量；若否，则key为{symbol}.{pair}
    :return:
    '''
    for pair in pairs_list:
        queue_name = '{symbol}.{pair}'.format(symbol=symbol, pair=pair)
        if multi:
            # 默认一个币对信息产生两个key,用于批量匹配.
            await consumer.register(callback, queue_name, exchange, routing_key='{symbol}.#'.format(symbol=symbol))
            await consumer.register(callback, queue_name, exchange, routing_key='#.{pair}'.format(pair=pair))
        else:
            await consumer.register(callback, queue_name, exchange, routing_key=queue_name)


async def market_pair_publish(channel, body, envelope, properties):
    '''
    根据 routing_key，获取变化币种，并推送给相应关注的用户

    routing-key：币种.币对
            e.g. 'BTC.BTC/USDT'
    Payload：传送json内必须包含exchange属性
            - e.g.：'huobi'，'aggregation'表明为聚合数据
            - {"exchange":"aggregation"}
    user_infos ：{ 'MarketPair': {user-client-class:{'category':2,'star':["BTC/USDT.huobi"]},}}

    category 判断用户关注内容
    - user,user_dic = user-client-class,{'category':2,'star':["BTC/USDT.huobi"]}
    - if category = 0 直接推送,仅推送聚合数据
    - if category = 1或2 判断star是否匹配
        - 1 推送单币种的所有信息（聚合和交易所）
        - 2 推送用户订阅的信息，指定币对+指定交易所,BTC/USDT.aggregation

    :param channel:通道
    :param body:Exchange 传输信息本体
    :param envelope:存储mq相关基础信息，例如 routing-key
    :param properties:
    '''
    currency, pair = envelope.routing_key.split('.')
    data = gzip.compress(body)
    data_dic = json.loads(str(body, encoding='utf-8'))
    query_name = "%s.%s" % (pair, data_dic['exchange'])
    for user, user_dic in user_infos['MarketPair'].items():
        if user_dic['category'] == 0 and data_dic['exchange'] == 'aggregation':
            user.write_message(data, binary=True)
        elif user_dic['category'] == 1 and currency in user_dic['star']:
            user.write_message(data, binary=True)
        elif user_dic['category'] == 2 and query_name in user_dic['star']:
            user.write_message(data, binary=True)
