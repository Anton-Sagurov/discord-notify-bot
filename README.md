# DiscordNotifyBot
This Discord bot sends notifications to Telegram when member on Discrord server changes his status on a voice channel (join/leave channel, muted/unmuted, and other [events](https://github.com/Anton-Sagurov/discord-notify-bot/blob/main/config.yaml#L12)). Also this bot handles the commands `/who` and returns the list of all active users joined any voice channel on Discrod Server.  
Motivation - this bot simply helps to know when your friends joined Discord Server without having to launch the Discord app and see who is online or asking them in messenger. You just always know who is online because notification sent automaticaly. Or you can just ask bot - `/who` is online.  
### How it works
There are 2 parts:
1. This Discord Notification Bot
2. [telegram-notify-bot](https://github.com/Anton-Sagurov/telegram-notify-bot)


### Notification events
As it was said - there are a list of [events](https://github.com/Anton-Sagurov/discord-notify-bot/blob/main/config.yaml#L12) that could send notifications to Telegram. The most useful and straightforward are - **join** and  notifications.

### Deployment
#### Run docker container
The docker image: `sagurov/discord-notification-bot:latest`

### Development
#### Requirements
Recommended python version >= 3.10

#### Install dependencies
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r ./requirements.txt
```

##### Run the bot
1. Export the `DISCORD_TOKEN` and `DISCORD_GUILD` environment variables
```bash
export DISCORD_TOKEN='XXXXXXXXXXXXXXXXXXXXXXXX.YYYYYY.zzzzzzzzzzzzzzzzzzzzzzzzzzz'
export DISCORD_GUILD='My awesome Discord server name'
```
2. Run the ds-notify-bot:
```bash
python -m ds-notify-bot
```
