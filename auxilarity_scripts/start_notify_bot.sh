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
           "${IMAGE_NAME}:${VERSION}" \
                --ds-token "${DISCORD_TOKEN}" \
                --ds-guild "${DISCORD_GUILD}" \
                --tg-token "${TG_TOKEN}" \
                --tg-chat-id "${TG_CHAT_ID}" \
                --notify-event join
