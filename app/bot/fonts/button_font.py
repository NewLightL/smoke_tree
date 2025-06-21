from app.core import load_config


settings = load_config()

class StartButtonFont:
    catalog = "🏷️ Каталог"
    callback_catalog = "catalog"
    channel = "📢 Наш канал"
    callback_channel = settings.link.url_channel


class CatalogButtonFont:
    filter = "🔍 Фильтр"
    callback_filter = "filter"
    search_by_name = "✏️ Найти по названию товара"
    callback_search_by_name = "search_by_name"
    search = "🚀 Поиск"
    callback_search = "search"


class FiltersButtonFont:
    taste = "🍏 Вкус"
    callback_taste = "taste"
    brand = "🏷️ Бренд"
    callback_brand = "brand"
    volume = "🧴 Объем"
    callback_volume = "volume"
    fortress = "Крепость"
    callback_fortress = "fortress"
    chill = "🧊 Холодок"
    callback_chill = "chill"
    type_nicotine = "🧪 Тип никотина"
    callback_type_nicotine = "type_nicotine"
    price = "💲 Цена"
    callback_price = "price"
    apply = "✅ Применить"
    callback_apply = "apply"

    @property
    def get_all_callback(self) -> list[str]:
        lst_callback = [callback for callback in dir(self)
                        if callback.startswith("callback")]
        return lst_callback
