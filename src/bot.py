"""Bot for the application."""

from os import listdir
from time import time
from logging import getLogger

from discord import Intents
from discord.ext import commands

from logs import setup_logs

log = getLogger(__name__)


class Bot(commands.Bot):
    """The Discord bot for the application."""

    def __init__(self):
        intents = Intents.all()
        super().__init__(command_prefix="."  ,intents=intents)

        self._start_timestamp = time()

        self.logs_filepath = setup_logs()
        self.commands_synced = False

    async def sync_app_commands(self):
        """Sync app commands with discord."""

        log.info("syncing app commands")
        await self.wait_until_ready()

        if not self.commands_synced:
            await self.tree.sync()
            self.commands_synced = True
            log.info("app commands synced")

    async def on_ready(self):
        log.info("bot is online")
        await self.sync_app_commands()

    async def load_extensions(self):
        """Load all of the bot extensions."""

        log.info("loading extensions")
        for filename in listdir("./src/ext"):
            if not filename.endswith(".py"):
                continue

            await self.load_extension(f"ext.{filename[:-3]}")
            log.info("loaded extension '%s'", filename)
