from configparser import ConfigParser


class Config:
    def __init__(self, config_file_path: str):
        config = ConfigParser()
        config.read(config_file_path)

        self.API_TOKEN = config.get('telegram', 'api_token')
        self.PROXY_URL = config.get('proxy', 'url')
        self.WEBHOOK_HOST = config.get('webhook', 'host')
        self.WEBAPP_HOST = config.get('app', 'host')
        self.WEBAPP_PORT = config.get('app', 'port')
        self.REDIS_HOST = config.get('redis', 'host')
        self.WEBHOOK_PATH = '/' + self.API_TOKEN
        self.WEBHOOK_URL = f'{self.WEBHOOK_HOST}{self.WEBHOOK_PATH}'
