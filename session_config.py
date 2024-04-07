import toml

from telethon import TelegramClient

with open('./config.toml') as config:
    config = toml.load(config)['app']

class SessionConfig:
    api_id = config['api_id']
    api_hash = config['api_hash']
    
    client = TelegramClient(
        'my_session',
        api_id,
        api_hash
    )
