"""Entry point for the bot application."""

import asyncio
from bot import Bot

async def main():
    with open("TOKEN", "r") as file:
        token = file.read()

    async with Bot() as bot:
        await bot.load_extensions()
        await bot.start(token=token, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())
