import os
from typing import Optional
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Telegram:
    BOT_TOKEN: str
    ADMIN_ID: int
    CHANNEL_ID: int


@dataclass
class Trello:
    API_KEY: str
    TOKEN: str
    BOARD_ID: str
    CALLBACK_WEBHOOK_ID: Optional[str]


@dataclass
class Configs:
    APP_URL: str
    trello: Trello
    telegram: Telegram


def load_config():
    return Configs(
        APP_URL=os.environ.get('APP_URL'),
        telegram=Telegram(
            BOT_TOKEN=os.environ.get('BOT_TOKEN'),
            ADMIN_ID=os.environ.get('ADMIN_ID'),
            CHANNEL_ID=os.environ.get('CHANNEL_ID'),
        ),
        trello=Trello(
            API_KEY=os.environ.get('TRELLO_API_KEY'),
            TOKEN=os.environ.get('TRELLO_TOKEN'),
            BOARD_ID=os.environ.get('BOARD_ID'),
            CALLBACK_WEBHOOK_ID=None,
        ),
    )


if os.environ.get('PROD'):
    load_dotenv('.env.prod')
else:
    load_dotenv('.env')


config = load_config()