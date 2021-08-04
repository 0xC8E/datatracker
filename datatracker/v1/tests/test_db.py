import asyncio

from datatracker.v1.data import datapoints


async def run():
    await add_points()
    print(await get_points())


async def add_points():
    for i in range(10):
        await datapoints.add_and_prune(i)


async def get_points():
    return await datapoints.get_latest()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
