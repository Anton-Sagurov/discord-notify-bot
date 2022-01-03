import os
import logging

from .bot import DiscordNotifyBot

if __name__ == "__main__":

    TOKEN = os.getenv("DISCORD_TOKEN")
    GUILD = os.getenv("DISCORD_GUILD")
    LOG_LEVEL = os.getenv("DISCORD_LOG_LEVEL")
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    logging.basicConfig(
        level=LOG_LEVEL, format="%(asctime)s %(levelname)s: %(message)s"
    )
    logger = logging.getLogger("DiscordNotifyBot")

    notify = DiscordNotifyBot(TOKEN, GUILD, logger, TG_TOKEN, TG_CHAT_ID)
    notify.start()
