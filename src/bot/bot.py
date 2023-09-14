from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src import config
from src.bot.handlers.start import router
from src.bot.middlewares.config import ConfigMiddleware




storage = MemoryStorage()
bot = Bot(token=config.telegram.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=storage)

# Register middlewares
dp.update.outer_middleware(ConfigMiddleware(config))

# Register routes
dp.include_router(router)
