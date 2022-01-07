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

    def __get_guild(self) -> discord.Guild:
        guild = discord.utils.get(self.client.guilds, name=self.guild_name)
        return guild

    def __get_channel_event(
        self, vostate_before: discord.VoiceState, vostate_after: discord.VoiceState
    ) -> dict:

        logging.debug(f"vostate_after: {vostate_after}")
        logging.debug(f"vostate_before: {vostate_before}")

        chnl_event = {
            "chnl_name": None,
            "chnl_guild_id": None,
            "type": None,
        }

        if vostate_after.channel is not None:
            chnl_event["guild_id"] = vostate_after.channel.guild.id
            chnl_event["name"] = vostate_after.channel.name
            chnl_event["type"] = "voice_channel_state_changed_after"
        elif vostate_before.channel is not None:
            chnl_event["guild_id"] = vostate_before.channel.guild.id
            chnl_event["name"] = vostate_before.channel.name
            chnl_event["type"] = "voice_channel_state_changed_before"

        return chnl_event

    def __get_voice_chnl_notification(
        self,
        member: str,
        vostate_before: discord.VoiceState,
        vostate_after: discord.VoiceState,
    ) -> dict:

        notification = {"notify": False, "message": ""}

        bot_guild = self.__get_guild()
        logging.debug(f"Config bot guild ID {bot_guild.id} ({bot_guild.name})")

        chnl_event = self.__get_channel_event(vostate_before, vostate_after)
        logging.info(
            f'Event: {chnl_event["type"]}; '
            f'Channel: {chnl_event["name"]}; '
            f'Guild ID: {chnl_event["guild_id"]}; '
            f"Member: {member};"
        )

        if chnl_event["guild_id"] == bot_guild.id:
            notification["notify"] = True

        if chnl_event["type"] == "voice_channel_state_changed_before":
            notification[
                "message"
            ] = f'{member} leave channel {chnl_event["name"]} server: {bot_guild.name}'
        elif chnl_event["type"] == "voice_channel_state_changed_after":
            notification[
                "message"
            ] = f'{member} joined channel {chnl_event["name"]} server: {bot_guild.name}'
        else:
            chnl_event["notify"] = False

        return notification

    def start(self):
        load_dotenv()

        @self.client.event
        async def on_ready():
            self.logger.info(f"Bot started. Guild name: {self.guild_name}")

        @self.client.event
        async def on_voice_state_update(member, vostate_before, vostate_after):
            notification = self.__get_voice_chnl_notification(
                member, vostate_before, vostate_after
            )
            if notification["notify"]:
                self.send_to_tg(notification["message"])

        self.client.run(self.token)

    def send_to_tg(self, message):
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
        if r.status_code != 200:
            self.logger.error(f"status code: {r.status_code}, text: {r.text}")
        else:
            self.logger.debug(f"message sent: {message}")
