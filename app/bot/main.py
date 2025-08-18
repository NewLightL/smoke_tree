from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core import load_config, redis_backend


settings = load_config()


bot = Bot(token=settings.bot.bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

storage = RedisStorage(redis=redis_backend)
dp = Dispatcher(storage=storage)
