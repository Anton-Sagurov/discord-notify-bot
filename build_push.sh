#!/usr/bin/env bash

IMAGE_NAME='sagurov/discord-notification-bot !'
VERSION=$(<./VERSION )

if [ -z "$VERSION" ];then
  "$VERSION is not defined"
  exit 1
fi

docker build . -t "$IMAGE_NAME:$VERSION"
docker push "$IMAGE_NAME:$VERSION"
