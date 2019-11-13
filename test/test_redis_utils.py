import pytest
from lib.redis import redis_utils


# pytest test
@pytest.mark.asyncio
async def test_ping():
    redis = await redis_utils.RedisPool.create(url='redis://localhost/', from_config=False)
    conn = await redis.get_conn()
    val = await conn.ping()
    assert val != 'PONG'
