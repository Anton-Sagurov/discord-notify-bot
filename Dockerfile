FROM python:3.10-alpine

ENV DISCORD_TOKEN="token"
ENV DISCORD_GUILD="My Awesome Discrod server name"

# ENV variables for building the image
ENV USER="dsbot"
ENV UID="1000"
ENV GID="1000"
ENV HOME="/opt/app"

RUN mkdir "$HOME" && \
    chown "$UID:$GID" "$HOME" && \
    addgroup -g "$GID" "$USER" && \
    adduser \
    --disabled-password \
    --gecos "" \
    --home "$(pwd)" \
    --ingroup "$USER" \
    --no-create-home \
    --uid "$UID" \
    "$USER"

USER "$USER"

COPY ./ds-notify-bot ./requirements.txt ./config.yaml ./config-schema.yaml "$HOME/ds-notify-bot/"
WORKDIR "$HOME"
# Modify the $USER PATH variable
ENV PATH="$PATH:$HOME/.local/bin"

RUN python -m pip install --user --no-cache-dir -r ./ds-notify-bot/requirements.txt

ENTRYPOINT ["python", "-m", "ds-notify-bot"]
