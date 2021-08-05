import os

import httpx

from . import metrics

PUBLIC_KEY = os.getenv("CRYPTOWATCH_PUBLIC_KEY")
SECRET_KEY = os.getenv("CRYPTOWATCH_SECRET_KEY")

MARKET = "bitfinex"


async def get_current_price(metric_id):
    async with httpx.AsyncClient() as client:
        result = await client.get(
            f"https://api.cryptowat.ch/markets/{MARKET}/{metric_id}/price",
            headers={"X-CW-API-Key": PUBLIC_KEY},
        )
        return result.json()["result"]["price"]
