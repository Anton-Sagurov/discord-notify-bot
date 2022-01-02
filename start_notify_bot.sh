#!/usr/bin/env bash

IMAGE_NAME='sagurov/discord-notification-bot'
VERSION=$(<./VERSION)
CONTAINER_NAME="ds-notify-bot"

DISCORD_TOKEN=''
DISCORD_GUILD=''

docker stop "$CONTAINER_NAME"
docker rm "$CONTAINER_NAME"

docker run -d --name "$CONTAINER_NAME" \
           -e DISCORD_TOKEN="${DISCORD_TOKEN}" \
           -e DISCORD_GUILD="${DISCORD_GUILD}" \
           "${IMAGE_NAME}:${VERSION}"
