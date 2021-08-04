import asyncio
import datetime
import statistics

from datatracker.v1.data import crypto_prices
from datatracker.v1.data import metrics

SECONDS_DELAY = 5


def run():
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Got kill signal; stopping.")


async def main_loop():
    print(f"Fetching and storing price at {datetime.datetime.now()}")
    for metric in metrics.get_all_metrics():
        asyncio.create_task(update_metric(metric))
    await asyncio.sleep(SECONDS_DELAY)
    await main_loop()


async def update_metric(metric):
    metric_id = metrics.get_metric_id(metric)
    price = await crypto_prices.get_current_price(metric_id)
    await metrics.add_and_prune(metric_id, price)
    sd = await metrics.compute_stdev(metric_id)
    await metrics.update_stdev(metric_id, sd)


if __name__ == "__main__":
    run()
