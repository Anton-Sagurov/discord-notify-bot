import json
import logging

import discord
from discord.ext import commands
import requests
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
            ]
        }
        self.token = token
        self.guild_name = guild_name
        self.client = discord.Client()
        self.bot = commands.Bot(command_prefix="!")
        self.tg_notify = True
        self.logger = logger
        self.tg_token = tg_token
        self.tg_chat_id = tg_chat_id
        self.tg_url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"

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

    async def __exec_command_who(self, ctx: discord.ext.commands.Context):
        active_users = await self.get_active_users()
        notification_message = []
        for channel in active_users:
            user_names = [n.name for n in active_users[channel]]
            answer = f"CHANNEL: {channel}\t USERS: {', '.join(user_names)}"
            self.logger.debug(answer)
            notification_message.append(answer)

        if not notification_message:
            notification_message = ["No one is online"]

        await ctx.send(content="\n".join(notification_message))
        if self.tg_notify:
            self.send_to_tg("\n".join(notification_message))

    async def get_active_users(self) -> dict:
        active_users = {}
        guild = self.__get_guild()

        for channel in guild.voice_channels:
            channel_users = await self.__get_channel_members(channel)
            if channel_users:
                self.logger.debug(f"channel: {channel}, user: {channel_users}")
                active_users.update({channel: channel_users})

        return active_users

    async def __get_channel_members(self, channel: discord.VoiceChannel) -> list:
        channel_members = []
        member_ids = channel.voice_states.keys()

        for id in member_ids:
            user = await self.bot.fetch_user(id)
            channel_members.append(user)

        return channel_members

    def __get_guild(self) -> discord.Guild:
        guild = discord.utils.get(self.bot.guilds, name=self.guild_name)
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

        @self.bot.event
        async def on_ready():
            self.logger.info(f"Bot started. Guild name: {self.guild_name}")

        @self.bot.event
        async def on_voice_state_update(member, vostate_before, vostate_after):
            notification = self.__get_voice_chnl_notification(
                member, vostate_before, vostate_after
            )
            self.logger.info(f"notification: {notification}")
            if notification["notify"]:
                self.logger.info(f'notification["notify"]: {notification["notify"]}')
                self.send_to_tg(notification["message"])

        @self.bot.event
        async def on_message(message: discord.Message) -> None:
            """
            Process Bot commands with messages to allow Bot process webhook messages

            :param message:
            :return: None
            """
            ignore: bool = False
            ctx: discord.ext.commands.Context = await self.bot.get_context(message)
            try:
                message_guid_id = message.guild.id
                message_guid_name = message.guild.name
            except AttributeError:
                self.logger.debug("No message.guild: {message}")
                message_guid_id = None
                message_guid_name = None

            bot_guild = self.__get_guild()

            if message_guid_id != bot_guild.id:
                ignore = True
                self.logger.debug(
                    f"message guild id: {message_guid_id}; "
                    f"bot guild id {bot_guild.id}; "
                    f"ignore: {ignore}"
                )
                self.logger.debug(
                    f"ignore command: '!who'; "
                    f"requested by: {message.author}; "
                    f"Guild: '{message_guid_name}' ({message_guid_id})"
                )

            if (message.content == "!who") and (ignore is False):
                self.logger.info(
                    f"exec command: '!who'; "
                    f"requested by: {message.author}; "
                    f"Guild: '{message_guid_name}' ({message_guid_id})"
                )
                await self.__exec_command_who(ctx)

        self.bot.run(self.token)
