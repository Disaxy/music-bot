import asyncio
from os.path import abspath, dirname, join

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.markdown import bold, code, italic, pre, text
from loguru import logger

from .configure import Config
from .middlewares import AccessMiddleware


config_file_path = join(dirname(abspath('main.py')), 'config.ini')
config = Config(config_file_path)

loop = asyncio.get_event_loop()
bot = Bot(config.API_TOKEN, proxy=config.PROXY_URL,
          parse_mode=ParseMode.MARKDOWN_V2)
# storage = RedisStorage2(config.REDIS_HOST)
dp = Dispatcher(bot, loop=loop)


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(text='Hello')


async def on_startup(dp: Dispatcher):
    logger.info('Bot started')
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    logger.info('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('Bye!')
