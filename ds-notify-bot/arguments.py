import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", dest="CONFIG", default=None, type=str)
parser.add_argument(
    "-s", "--schema", dest="SCHEMA", default="config-schema.yaml", type=str
)
parser.add_argument(
    "--log-format",
    dest="LOGFRMT",
    default="%(asctime)s %(levelname)s: %(message)s",
    type=str,
    help="logging.basicConfig(format="")"
)
parser.add_argument("-l", "--log-level", dest="LOGLVL", default="INFO", type=str)
parser.add_argument("--ds-token", dest="DS_TOKEN", default=None, type=str,
                    help="Discrod Bot token")
parser.add_argument("--ds-guild", dest="DS_GUILD", default=None, type=str,
                    help="Discord guild(server) name.")
parser.add_argument("--tg-token", dest="TG_TOKEN", default=None, type=str,
                    help="Telegram bot token to send messages")
parser.add_argument("--tg-chat-id", dest="TG_CHAT_ID", default=None, type=str,
                    help="Telegram chat id where to send notifications")
parser.add_argument("--notify-event", dest="NOTIFY_EVENTS", nargs="+", default=["join"],
                    help=f"List of Discord Voice Channel events to notify when happen:" 
                         f"[join, leave, change, muted, unmuted, deaf, undeaf, " 
                         f"'start stream', 'finish stream', 'video on', 'video off']. "
                         f"By default notify only on member join Voice Channel")

ARGS = parser.parse_args()
