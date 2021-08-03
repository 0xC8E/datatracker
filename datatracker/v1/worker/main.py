import asyncio
import httpx
import datetime


SECONDS_DELAY = 10


def run():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main_loop())
    except KeyboardInterrupt:
        print("Got kill signal; stopping.")


async def main_loop():
    while True:
        print(f"Starting at {datetime.datetime.now()}")
        await asyncio.sleep(SECONDS_DELAY)
        asyncio.create_task(fetch_and_store_stats())


async def fetch_and_store_stats():
    await asyncio.sleep(1)
    stats = await fetch_stats()
    await store(stats)


async def fetch_stats():
    async with httpx.AsyncClient() as client:
        result = await client.get("https://www.example.com/")
        return result


async def store(stats):
    print(f"Storing at {datetime.datetime.now()}.")


if __name__ == "__main__":
    run()
