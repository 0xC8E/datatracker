import decimal
import datetime

import aioredis

REDIS_URL = "redis://localhost/"
MAIN_DB = 1
TEST_DB = 2

RANGE_KEY = "dt:datapoints"

DEFAULT_HOURS = 24


connection = aioredis.from_url(REDIS_URL, db=MAIN_DB)


async def connect_for_testing_and_clear():
    print("Warning - Using test database in current process.")
    global connection
    connection = aioredis.from_url(REDIS_URL, db=TEST_DB)
    await connection.delete(RANGE_KEY)


async def get_latest(hours=DEFAULT_HOURS):
    range_start = datetime.datetime.now() - datetime.timedelta(hours=hours)

    return await connection.zrangebyscore(
        RANGE_KEY,
        min=range_start.timestamp(),
        max="+inf",
        withscores=True,
        score_cast_func=float,
    )


async def add_and_prune(data_point, hours=DEFAULT_HOURS):
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)

    async with connection.pipeline(transaction=True) as pipeline:
        pipeline.zadd(RANGE_KEY, {data_point: now.timestamp()})
        pipeline.zremrangebyscore(
            RANGE_KEY, min="-inf", max=f"({range_start.timestamp()}"
        )
        result = await pipeline.execute()

    # all_items = await connection.zrange(RANGE_KEY, start=0, end=-1, withscores=True)
    # breakpoint()
    return result
