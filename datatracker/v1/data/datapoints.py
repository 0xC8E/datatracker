import datetime
import functools

import aioredis

REDIS_URL = "redis://localhost/1"

RANGE_KEY = "dt:datapoints"

DEFAULT_HOURS = 24


@functools.lru_cache()
async def _connect():
    return aioredis.from_url(REDIS_URL)


async def get_latest(hours=DEFAULT_HOURS):
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)
    connection = await _connect()
    return await connection.zrangebyscore(
        RANGE_KEY, range_start.timestamp(), now.timestamp()
    )


async def add_and_prune(data_point, hours=DEFAULT_HOURS):
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)
    connection = await _connect()
    async with connection.pipeline(transaction=True) as pipeline:
        pipeline.zadd(RANGE_KEY, data_point, now)
        pipeline.zremrangebyscore(RANGE_KEY, -1, range_start)
        result = pipeline.execute()
    return await result
