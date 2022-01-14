import logging

import jsonschema
import yaml

from .bot import DiscordNotifyBot
from .arguments import ARGS


def get_config_from_args() -> dict:
    config = {
        "discord": {
            "token": ARGS.DS_TOKEN,
            "guild": ARGS.DS_GUILD,
        },
        "bot": {
            "loglevel": ARGS.LOGLVL,
        },
        "notification": {
            "tg_token": ARGS.TG_TOKEN,
            "tg_chat_id": ARGS.TG_CHAT_ID,
            "events": ARGS.NOTIFY_EVENTS
        },
    }
    return config


def get_config_from_file(config_file: str, schema_file: str) -> dict:

    with open(schema_file, "r") as schema_file:
        _schema = yaml.safe_load(schema_file)

    with open(config_file, "r") as config_file:
        config = yaml.safe_load(config_file)

    jsonschema.validate(config, _schema)
    return config


if __name__ == "__main__":

    if ARGS.CONFIG:
        config = get_config_from_file(ARGS.CONFIG, ARGS.SCHEMA)
    else:
        config = get_config_from_args()

    logging.basicConfig(level=config["bot"]["loglevel"], format=ARGS.LOGFRMT)
    logger = logging.getLogger("DiscordNotifyBot")
    logger.debug(f"config: {config}")

    notify = DiscordNotifyBot(
        config["discord"]["token"],
        config["discord"]["guild"],
        logger,
        config["notification"]["tg_token"],
        config["notification"]["tg_chat_id"],
    )
    notify.start()
