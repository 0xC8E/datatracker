import asyncio
import datetime

from datatracker.v1.data import crypto_prices
from datatracker.v1.data import datapoints

SECONDS_DELAY = 60


def run():
    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print("Got kill signal; stopping.")


async def main_loop():
    print(f"Fetching and storing price at {datetime.datetime.now()}")
    asyncio.create_task(fetch_and_store_price())
    await asyncio.sleep(SECONDS_DELAY)
    await main_loop()


async def fetch_and_store_price():
    price = await crypto_prices.get_current_price()
    await datapoints.add_and_prune(price)


if __name__ == "__main__":
    run()
