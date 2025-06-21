from app.core import load_config


settings = load_config()

class StartButtonFont:
    catalog = "Каталог"
    callback_catalog = "catalog"
    channel = "Наш канал"
    callback_channel = settings.link.url_channel
