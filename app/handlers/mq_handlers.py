from tornado import gen

from lib.base import APIHandler


class MQProducerHander(APIHandler):
    @gen.coroutine
    def get(self):
        mq = self.application.mq
        exchange_name = 'test'
        data = "hello,mq"
        # yield mq.producer(exchange_name,'fanout')
        yield mq.publish(data, exchange_name)
        self.write(self.success_json(data))


class MQConsumerHander(APIHandler):
    @gen.coroutine
    def get(self):
        mq = self.application.mq
        exchange_name = 'test'
        queue_name = 'mq_test'
        yield mq.consumer(queue_name, exchange_name, routing_key='', prefetch_count=1)
        yield mq.subscribe(self.mytest, queue_name)
        self.write(self.success_json("hello"))

    async def mytest(self, *args, **kwargs):
        print(args)
        print(kwargs)
        print('hello mq consumer!')
