import datetime
import statistics

import aioredis

REDIS_URL = "redis://localhost/"
MAIN_DB = 1
TEST_DB = 2

DEFAULT_HOURS = 24

RANGE_KEY = "dt:data_points"
STDEVS_KEY = "dt:stdevs"

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


def _get_range_key(metric_id):
    return f"{RANGE_KEY}:{metric_id}"


def _get_stdevs_key():
    return STDEVS_KEY


async def connect_for_testing_and_clear():
    print("Warning - Using test database in current process.")
    global connection
    connection = aioredis.from_url(REDIS_URL, db=TEST_DB)

    await connection.flushdb()


async def get_latest(metric_id, hours=DEFAULT_HOURS):
    key = _get_range_key(metric_id)
    range_start = datetime.datetime.now() - datetime.timedelta(hours=hours)

    return await connection.zrangebyscore(
        key,
        min=range_start.timestamp(),
        max="+inf",
        withscores=True,
        score_cast_func=float,
    )


async def add_and_prune(metric_id, data_point, hours=DEFAULT_HOURS):
    key = _get_range_key(metric_id)
    now = datetime.datetime.now()
    range_start = now - datetime.timedelta(hours=hours)

    async with connection.pipeline(transaction=True) as pipeline:
        pipeline.zadd(key, {data_point: now.timestamp()})
        pipeline.zremrangebyscore(key, min="-inf", max=f"({range_start.timestamp()}")
        result = await pipeline.execute()

    return result


async def compute_stdev(metric_id):
    current_data = await get_latest(metric_id)
    try:
        sd = statistics.stdev([float(p[0]) for p in current_data])
    except statistics.StatisticsError:
        return 0

    return sd


async def update_stdev(metric_id, stdev):
    key = _get_stdevs_key()

    return await connection.zadd(
        key,
        {metric_id: stdev},
    )


async def get_all_stdevs():
    key = _get_stdevs_key()

    return await connection.zrangebyscore(key, min="-inf", max="+inf", withscores=True)


async def get_rank(metric_id):
    all_stdevs = await get_all_stdevs()
    rank = -1
    for i, item in enumerate(all_stdevs):
        item_id = item[0]
        if item_id == metric_id.encode("utf-8"):
            rank = i + 1
            break
    return rank
