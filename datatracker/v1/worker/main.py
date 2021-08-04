import asyncio
import datetime

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
        asyncio.create_task(fetch_and_store_price(metric))
    await asyncio.sleep(SECONDS_DELAY)
    await main_loop()


async def fetch_and_store_price(metric):
    price = await crypto_prices.get_current_price(metric)
    await metrics.add_and_prune(metric, price)


if __name__ == "__main__":
    run()
