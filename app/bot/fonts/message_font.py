class MessageFont:
    start = "<b>Привет!</b>👋\n\nЭто бот <b>SmokeTree</b>, здесь ты можешь приобрести "\
        "жидкости для вейпов\n\nСмотри каталог по кнопке внизу и выбирай, что по душе💗"


class CatalogFont:
    introductory_page = "Выбери фильтры или начни сразу смотреть каталог по кнопкам снизу"
    filters_page = "Выбери фильтры"
    filter_page = "Выбери значение фильтра"
    write_price = "Введи максимальную цену товара"
    not_correct_price = "Ты ввел что-то не то, поробуй еще раз"
    end_of_select_price = "Ты ввел цену"

    @classmethod
    def user_price(cls, price: int|None = None) -> str:
        if price is None:
            return cls.write_price
        return f"{cls.write_price}\n\nИщем товары по цене до {price}"


class SearchFont:
    search_product = "Выбери товар"
    last_products = "🔥<b>ОСТАЛОСЬ В НАЛИЧИИ</b>🔥"
    more_products = "✅ Есть в наличии"
    card_item = "<b>{}</b>\n\n🏷️ Бренд - {}\n🍏 Вкус - {}\n🧴 Объем - {}\n💪 Крепость - {}\n"\
        "🧪 Тип никотина - {}\n"\
        "🧊 Холодок - {}\n\n{} - {}шт\n\n💰 Цена - {}"
    search_by_name = "Введи название товара"
    incorrect_name = "Не существует такого товара"


class BasketFont:
    card_basket = "<b>🛒 Корзина</b>\n\nТвои товары:\n\n<code>{}\nОбщая цена: {}р.</code>\n\n"\
                "Отправь этот текст админу: скопируй текст и нажми на кнопку снизу"
    card_products_in_basket = "<b>{}</b>\n\n🏷️ Бренд - {}\n🍏 Вкус"\
        " - {}\n🧴 Объем - {}\n💪 Крепость - {}\n"\
        "🧪 Тип никотина - {}\n"\
        "🧊 Холодок - {}\n\n{} - {}шт\n\n💰 Цена - {}\n"\
        "📦 В корзине - {}шт"
    basket_is_empty = "<b>Корзина пуста</b>\n\nПереходи в каталог и добавь товары"
