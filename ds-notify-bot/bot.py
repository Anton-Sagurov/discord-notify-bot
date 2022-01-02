import logging
from datetime import datetime

import discord
from dotenv import load_dotenv


class DiscordNotifyBot:
    def __init__(
        self,
        token: str,
        guild_name: str,
        logger: logging.Logger,
    ):
        self.token = token
        self.guild_name = guild_name
        self.client = discord.Client()
        self.logger = logger

    def start(self):
        load_dotenv()

        @self.client.event
        async def on_ready():
            guild = discord.utils.get(self.client.guilds, name=self.guild_name)
            self.logger.info(f"Bot connected to Guild: {guild}")

        @self.client.event
        async def on_voice_state_update(member, before, after):
            chn_before = "{0.channel}".format(before)
            chn_after = "{0.channel}".format(after)

            if chn_before == "None":
                self.logger.info(
                    f"{member} joined the voice channel: {chn_after}"
                )
            elif chn_after == "None":
                self.logger.info(
                    f"{member} left the voice channel: {chn_before}"
                )
            elif chn_before != chn_after:
                self.logger.info(
                    f"{member} changed the voice channel from {chn_before} to {chn_after}"
                )

        self.client.run(self.token)
