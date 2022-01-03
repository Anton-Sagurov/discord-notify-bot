import json
import logging
import requests

import discord
from dotenv import load_dotenv


class DiscordNotifyBot:
    def __init__(
        self,
        token: str,
        guild_name: str,
        logger: logging.Logger,
        tg_token: str = None,
        tg_chat_id: str = None,
    ):
        self.token = token
        self.guild_name = guild_name
        self.client = discord.Client()
        self.logger = logger
        self.tg_token = tg_token
        self.tg_chat_id = tg_chat_id
        self.tg_url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"

    def __get_voice_chnl_notification(
        self, member: str, before_state: str, after_state: str
    ) -> dict:
        notification = {"notify": True, "message": ""}
        if before_state == "None":
            notification[
                "message"
            ] = f"{member} joined the voice channel: {after_state}"
        elif after_state == "None":
            notification["message"] = f"{member} left the voice channel: {before_state}"
        else:
            notification["notify"] = False
        return notification

    def start(self):
        load_dotenv()

        @self.client.event
        async def on_ready():
            guild = discord.utils.get(self.client.guilds, name=self.guild_name)
            self.logger.info(f"Bot connected to Guild: {guild}")

        @self.client.event
        async def on_voice_state_update(member, before, after):
            notification = self.__get_voice_chnl_notification(
                member, "{0.channel}".format(before), "{0.channel}".format(after)
            )
            self.logger.info(notification["message"])
            if notification["notify"]:
                self.send_to_tg(notification["message"])

        self.client.run(self.token)

    def send_to_tg(self, message):
        self.logger.info(message)
        r = requests.post(
            url=self.tg_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {
                    "chat_id": self.tg_chat_id,
                    "text": message,
                    "disable_notification": "true",
                }
            ),
        )
        self.logger.info(f"status code: {r.status_code}, text: {r.text}")
