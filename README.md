# DiscordNotifyBot
Discord Bot to send notifications when user joing/leaving the Voice channel.

## Requirements
Recomended python version >= 3.10

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
