from aiogram.fsm.state import StatesGroup, State


class ViewCatalog(StatesGroup):
    view_introductory_page = State()
    view_filters = State()
    view_filter_parametr = State()
    search_by_name = State()
    select_price = State()
    view_items = State()
    card_item = State()