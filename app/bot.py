import asyncio
from os.path import abspath, dirname, join

from aiogram import Bot, Dispatcher, types
# from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils.executor import start_webhook
from aiogram.utils.markdown import bold, code, italic, pre, text
from loguru import logger

from configure import Config
from middlewares import AccessMiddleware
from parser import SounCloudDownloader


scp = SounCloudDownloader('https://www.forhub.io/download.php')


config_file_path = join(dirname(abspath('config.ini')), 'config.ini')
config = Config(config_file_path)

loop = asyncio.get_event_loop()
bot = Bot(config.API_TOKEN, proxy=config.PROXY_URL,
          parse_mode=ParseMode.MARKDOWN_V2)
# storage = RedisStorage2(config.REDIS_HOST)
dp = Dispatcher(bot, loop=loop)


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer(text='Кидай ссылку на тречик в soundcloud')


@dp.message_handler(state='*', content_types=['text'])
async def send_file(message: types.Message, state: FSMContext):
    await types.ChatActions.upload_audio()
    sc_path = message.text
    raw_link, title = await scp.get_link(sc_path)
    await bot.send_audio(message.chat.id, raw_link)


async def on_startup(dp: Dispatcher):
    logger.info('Bot started')
    await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    logger.info('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logger.info('Bye!')


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT,
                  skip_updates=True)
