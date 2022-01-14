#!/usr/bin/env bash

IMAGE_NAME='sagurov/discord-notification-bot'
VERSION=$(<./VERSION)
CONTAINER_NAME="ds-notify-bot"

DISCORD_TOKEN=""
DISCORD_GUILD=""
TG_TOKEN=""
TG_CHAT_ID=""
DISCORD_LOG_LEVEL=""

docker stop "$CONTAINER_NAME"
docker rm "$CONTAINER_NAME"

docker run -d --name "$CONTAINER_NAME" \
           -e DISCORD_TOKEN="${DISCORD_TOKEN}" \
           -e DISCORD_GUILD="${DISCORD_GUILD}" \
           -e DISCORD_LOG_LEVEL="${DISCORD_LOG_LEVEL}" \
           -e TG_TOKEN="${TG_TOKEN}"
           -e TG_CHAT_ID="${TG_CHAT_ID}"
           "${IMAGE_NAME}:${VERSION}"
