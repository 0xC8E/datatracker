import datetime

import aioredis

REDIS_URL = "redis://localhost/"
MAIN_DB = 1
TEST_DB = 2

DEFAULT_HOURS = 24

RANGE_KEY = "dt:data_points"
RANK_KEY = "dt:ranks"

METRICS = [
    ("Bitcoin in USD", "btcusd"),
    ("Bitcoin in EUR", "btceur"),
]

connection = aioredis.from_url(REDIS_URL, db=MAIN_DB)


def get_all_metrics():
    return METRICS


def get_metric_id(metric):
    return metric[1].strip().lower()


def get_readable_name(metric):
    return metric[0].strip()


async def connect_for_testing_and_clear():
    print("Warning - Using test database in current process.")
    global connection
    connection = aioredis.from_url(REDIS_URL, db=TEST_DB)
    await connection.flushdb()


def _get_key(metric):
    metric_id = get_metric_id(metric)
    return f"{RANGE_KEY}:{metric_id}"


async def get_latest(metric, hours=DEFAULT_HOURS):
    key = _get_key(metric)
    range_start = datetime.datetime.now() - datetime.timedelta(hours=hours)

    return await connection.zrangebyscore(
        key,
        min=range_start.timestamp(),
        max="+inf",
        withscores=True,
        score_cast_func=float,
    )


async def add_and_prune(metric, data_point, hours=DEFAULT_HOURS):
    key = _get_key(metric)
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)

    async with connection.pipeline(transaction=True) as pipeline:
        pipeline.zadd(key, {data_point: now.timestamp()})
        pipeline.zremrangebyscore(key, min="-inf", max=f"({range_start.timestamp()}")
        result = await pipeline.execute()

    return result
