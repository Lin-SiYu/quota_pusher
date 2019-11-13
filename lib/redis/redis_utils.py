import aioredis
import asyncio
from tornado.options import options


async def _init_with_loop(**kwargs):
    """
    redis 连接池
    :param loop: 事件循环
    :return: redis pool
    """
    _loop = kwargs.pop("loop", asyncio.get_event_loop())
    _url = kwargs.pop('url', None)
    assert _loop, "use get_event_loop()"
    assert _url, "url like redis://localhost/"
    __pool = await aioredis.create_redis_pool(_url, loop=_loop, encoding='utf8', **kwargs)
    return __pool


class RedisPool:

    @classmethod
    def from_config(cls):
        data = options.as_dict().copy()
        return dict(
            url=data.pop('REDIS_URL'),
            db=data.pop('REDIS_DB', None),
            password=data.pop('REDIS_PWD', None),
            minsize=data.pop('REDIS_MIN', 5),
            maxsize=data.pop('REDIS_MAX', 10),
        )

    @classmethod
    async def create(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            if kwargs.pop('from_config', True):
                kwargs = cls.from_config()
            cls._redis = await _init_with_loop(**kwargs)
            cls._instance = super(RedisPool, cls).__new__(cls)
        return cls._instance

    def get_conn(self) -> aioredis.Redis:
        return self._redis
