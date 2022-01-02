import os
import logging

from .bot import DiscordNotifyBot

if __name__ == "__main__":

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")

    logging.basicConfig(level="INFO")
    logger = logging.getLogger("DiscordNotifyBot")

    notify = DiscordNotifyBot(TOKEN, GUILD, logger)
    notify.start()
