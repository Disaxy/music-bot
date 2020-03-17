from aiogram.utils.executor import start_webhook
from app.bot import config, dp, on_shutdown, on_startup


if __name__ == '__main__':
    start_webhook(dispatcher=dp, webhook_path=config.WEBHOOK_PATH,
                  on_startup=on_startup, on_shutdown=on_shutdown,
                  host=config.WEBAPP_HOST, port=config.WEBAPP_PORT,
                  skip_updates=True)
