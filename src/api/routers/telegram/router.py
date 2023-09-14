import textwrap

from aiogram import Bot, Dispatcher, types

from fastapi import APIRouter, Request, HTTPException

from . import utils, services
from src import config
from src.bot import bot, dp



router = APIRouter(
    prefix='/telegram',
    tags=['Telegram']
)


@router.post(f'/bot/{config.telegram.BOT_TOKEN}')
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)



@router.get('/notify_admin')
async def notify_admin(message: str):
    await bot.send_message(chat_id=config.telegram.ADMIN_ID, text=message)


@router.get('/publich_channel')
async def public_channel(title: str, description: str, url: str):

    text = textwrap.dedent(f"""
    <b>{title}</b>

    {description}

    Подробно: {url}
    """)

    await bot.send_message(chat_id=config.telegram.CHANNEL_ID, text=text)
