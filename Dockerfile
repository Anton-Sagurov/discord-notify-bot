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

COPY ./ds-notify-bot ./requirements.txt "$HOME/"
WORKDIR "$HOME"

# Modify PATH variable
ENV PATH="$PATH:$HOME/.local/bin"

RUN python -m pip install --user --no-cache-dir -r requirements.txt

CMD ["python3"]
ENTRYPOINT ["-m", "ds-notify-bot"]
