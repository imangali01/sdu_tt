import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiohttp

from src import config
from src.api.routers import router as api_routers
from src.bot import bot, dp
from src.api.middlewares.trello import TrelloWebhookMiddleware



logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)



app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT", "HEAD"],
    allow_headers=["Content-Type", "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Authorization"],
)
TRELLO_WEBHOOK_URL = f"https://api.trello.com/1/webhooks"
app.add_middleware(TrelloWebhookMiddleware, trello_webhook_url=TRELLO_WEBHOOK_URL)

app.include_router(api_routers)


@app.on_event("startup")
async def on_startup():

    # config telegram bot webhook
    TELEGRAM_BOT_WEBHOOK_URL =  config.APP_URL + '/api/telegram/bot/' + config.telegram.BOT_TOKEN

    logger.info(TELEGRAM_BOT_WEBHOOK_URL)

    telegram_bot_webhook_info = await bot.get_webhook_info()
    if telegram_bot_webhook_info != TELEGRAM_BOT_WEBHOOK_URL:
        await bot.set_webhook(url=TELEGRAM_BOT_WEBHOOK_URL)

    logger.info("App started")


@app.on_event("shutdown")
async def on_shutdown():
    # stop telegram bot webhook
    await bot.session.close()

    # stop trello webhook
    URL = f"https://api.trello.com/1/webhooks/{config.trello.CALLBACK_WEBHOOK_ID}"

    payload = {
        "key": config.trello.API_KEY,
        "token": config.trello.TOKEN,
    }

    logger.info(f'[+] DELETING: {URL}\n{payload}')

    async with aiohttp.ClientSession() as session:
        async with session.delete(URL, json=payload) as response:
            result = await response.status
            logger.info(f'[+] RESPONSE: {result}')

    logger.info("App stopped")
