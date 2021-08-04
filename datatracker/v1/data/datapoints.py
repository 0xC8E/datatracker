import datetime

import aioredis

REDIS_URL = "redis://localhost/1"

RANGE_KEY = "dt:datapoints"

DEFAULT_HOURS = 24


connection = aioredis.from_url(REDIS_URL)


async def get_latest(hours=DEFAULT_HOURS):
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)
    return await connection.zrangebyscore(
        RANGE_KEY, range_start.timestamp(), now.timestamp(), withscores=True
    )


async def add_and_prune(data_point, hours=DEFAULT_HOURS):
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)
    async with connection.pipeline(transaction=True) as pipeline:
        pipeline.zadd(RANGE_KEY, {data_point: now.timestamp()})
        pipeline.zremrangebyscore(RANGE_KEY, -1, range_start.timestamp())
        result = await pipeline.execute()
    return result
