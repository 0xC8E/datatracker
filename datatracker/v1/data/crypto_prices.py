import os

import httpx

PUBLIC_KEY = os.getenv("CRYPTOWATCH_PUBLIC_KEY")
SECRET_KEY = os.getenv("CRYPTOWATCH_SECRET_KEY")


async def get_current_price():
    async with httpx.AsyncClient() as client:
        result = await client.get(
            "https://api.cryptowat.ch/markets/coinbase-pro/btcusd/price",
            headers={"X-CW-API-Key": PUBLIC_KEY},
        )
        return result.json()["result"]["price"]
