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
        self.notify_on = {
            "type": [
                "join",
                "leave",
                "change",
                "muted",
                "unmuted",
                "deaf",
                "undeaf",
                "start stream",
                "finish stream",
                "video on",
                "video off",
            ]
        }
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
        self, before: discord.VoiceState, after: discord.VoiceState
    ) -> dict:

        self.logger.debug(f"after: {after}")
        self.logger.debug(f"before: {before}")

        event = {
            "type": None,
            "channel_name": None,
            "channel_guild_name": None,
            "channel_guild_id": None,
        }

        if after.channel:
            channel = after.channel
        elif before.channel:
            channel = before.channel
        else:
            channel = None

        event["channel_name"] = channel.name
        event["channel_guild_name"] = channel.guild.name
        event["channel_guild_id"] = channel.guild.id

        if after.channel and before.channel is None:
            event["type"] = "join"
        elif before.channel and after.channel is None:
            event["type"] = "leave"
        else:
            event["type"] = "change"

        if after.self_mute and (not before.self_mute):
            event["type"] = "muted"
        elif (not after.self_mute) and before.self_mute:
            event["type"] = "unmuted"

        if after.self_deaf and (not before.self_deaf):
            event["type"] = "deaf"
        elif (not after.self_deaf) and before.self_deaf:
            event["type"] = "undeaf"

        if after.self_stream and (not before.self_stream):
            event["type"] = "start stream"
        elif (not after.self_stream) and before.self_stream:
            event["type"] = "finish stream"

        if after.self_video and (not before.self_video):
            event["type"] = "video on"
        elif (not after.self_video) and before.self_video:
            event["type"] = "video off"

        return event

    def __get_voice_chnl_notification(
        self,
        member: str,
        vostate_before: discord.VoiceState,
        vostate_after: discord.VoiceState,
    ) -> dict:

        notification = {"notify": False, "message": ""}

        bot_guild = self.__get_guild()
        self.logger.debug(f"Config bot guild ID {bot_guild.id} ({bot_guild.name})")

        chnl_event = self.__get_channel_event(vostate_before, vostate_after)
        self.logger.info(
            f'Event: {chnl_event["type"]}; '
            f'Channel: {chnl_event["channel_name"]}; '
            f'Guild name: {chnl_event["channel_guild_name"]}; '
            f'Guild ID: {chnl_event["channel_guild_id"]}; '
            f"Member: {member};"
        )

        notification[
            "message"
        ] = f'{member} {chnl_event["type"]} channel {chnl_event["channel_name"]} server: {bot_guild.name}'

        if chnl_event["channel_guild_id"] == bot_guild.id:
            self.logger.debug(f"channel event type: {chnl_event['type']}")
            if chnl_event["type"] in self.notify_on["type"]:
                notification["notify"] = True

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
            self.logger.info(f"notification: {notification}")
            if notification["notify"]:
                self.logger.info(f'notification["notify"]: {notification["notify"]}')
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
