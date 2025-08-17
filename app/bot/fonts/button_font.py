from app.core import load_config


settings = load_config()


class BaseButtonFont:
    apply = "✅ Применить"
    callback_apply = "apply"
    reset = "❌ Сбросить"
    callback_reset = "reset"
    right = "⏩"
    left = "⏪"


class StartButtonFont:
    catalog = "🏷️ Каталог"
    callback_catalog = "catalog"
    basket = "🛒 Корзина"
    callback_basket = "basket"
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
    fortress = "⚡ Крепость"
    callback_fortress = "fortress"
    chill = "🧊 Холодок"
    callback_chill = "chill"
    type_nicotine = "🧪 Тип никотина"
    callback_type_nicotine = "type_nicotine"
    price = "💲 Цена"
    callback_price = "price"  #! OTHER FUNCTION

    @classmethod
    def get_all_callback(cls) -> list[str]:
        lst_callback = [getattr(cls, callback) for callback in dir(cls)
                        if callback.startswith("callback") and
                        callback not in ("callback_apply", "callback_price")]
        return lst_callback


class SearchButtonFont:
    select_products = "🛒 Добавить в корзину"
    return_to_basket = "📦 К корзине"
    return_to_filters = "🔍 К фильтрам"
    return_to_home = "🏡 Домой"


class BasketButtonFont:
    return_to_filters = "🔍 К фильтрам"
    return_to_home = "🏡 Домой"
    plus = "+1"
    minus = "-1"
    confirm_order = "✅ Оформить заказ"
    write_admin = "👨‍💼 Написать админу"
