"""Main extension for the application."""

from time import time
from logging import getLogger

from discord import app_commands, Interaction as Inter, Message
from discord.ext import commands, tasks

log = getLogger(__name__)


class Extension(commands.Cog, name="Emojinary"):
    """Main extension for the application."""

    upload_queue: list[tuple[int, int]] = []

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_ready(self):
        log.info("extension '%s' is ready", self.qualified_name)

    @app_commands.command(name="check-queue")
    async def check_queue_cmd(self, inter: Inter):
        """Returns the upload queue."""

        output = ""
        for user_id, timestamp in self.upload_queue:
            output += f"{user_id} - {timestamp}"

        await inter.response.send_message(
            output or "Queue is empty"
        )

    @app_commands.command(name="upload")
    async def upload_cmd(self, inter: Inter):
        """Upload emoji to the application."""

        if inter.user.id not in self.upload_queue:
            self.upload_queue.append((inter.user.id, int(time())))

        await inter.response.send_message(
            "Please upload your emoji into this channel" \
            "\nI'll react with a :thumbsup: to show I've added it.",
            ephemeral=True
        )

    @commands.Cog.listener(name="on_message")
    async def find_uploads(self, message:Message):
        """Find user uploads."""

        conditions = (
            message.author.id in [item[0] for item in self.upload_queue],
            message.attachments,
        )

        if not all(condition for condition in conditions):
            return

        await message.add_reaction("👍")

        for item in self.upload_queue:
            if item[0] == message.author.id:
                self.upload_queue.remove(item)

    @tasks.loop(minutes=5)
    async def check_queue(self):
        """Check the queue and remove people waiting over X amount of time."""

        for item in self.upload_queue:
            if item[1] > time() - 300: # 5 minutes
                self.upload_queue.remove(item)


async def setup(bot: commands.Bot):
    """Add the extension to the bot."""

    await bot.add_cog(Extension(bot))
