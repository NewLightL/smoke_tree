from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.state.catalog_state import ViewCatalog
from app.bot.fonts.button_font import CatalogButtonFont, BaseButtonFont
from app.bot.fonts.message_font import SearchFont
from app.bot.fonts.call_font import CallAnswerFont
from app.bot.keyboars.search_keyboards import get_search_peg_keyboard
from app.bot.keyboars.base_keyboards import reset_search
from app.bot.callback.search_fabric import SearchAction, SearchCallback
from app.bot.utils.search import SearchUtils
from app.db import ProductsDAO, Products


router = Router()


@router.callback_query(F.data == BaseButtonFont.callback_apply,
                       StateFilter(ViewCatalog.view_filters))
@router.callback_query(F.data == CatalogButtonFont.callback_search,
                       StateFilter(ViewCatalog.view_introductory_page))
async def search_products(call: CallbackQuery, state: FSMContext):
    per_page = 0
    await call.answer(CallAnswerFont.apply)
    await state.set_state(ViewCatalog.view_items)
    data = await state.get_data()
    products = await ProductsDAO.select_products_by_filter(**data)

    if products is None:
        await call.message.edit_text(
        SearchUtils.create_message_for_item_card(products),
        reply_markup=await get_search_peg_keyboard(0, per_page))
        return

    product = products[per_page]
    await call.message.edit_media(InputMediaPhoto(
        media=SearchUtils.get_photo_products_by_id(product.photo), # type: ignore
        caption=SearchUtils.create_message_for_item_card(product),), # type: ignore
        reply_markup=await get_search_peg_keyboard(len(products), per_page)) # type: ignore


# @router.callback_query(StateFilter(ViewCatalog.view_items), # TODOs доделать кнопку выбора
#                        SearchCallback.filter(F.action == Action.select))
# async def view_product(call: CallbackQuery, state: FSMContext, callback_data: SearchCallback):
#     await call.answer()
#     await state.set_state(ViewCatalog.card_item)
#     product: Products = await ProductsDAO.select_by_id(callback_data.product_id)  # type: ignore
#     await call.message.edit_caption(SearchUtils.create_message_for_item_card(product))


@router.callback_query(StateFilter(ViewCatalog.view_items),
                       SearchCallback.filter(F.action == SearchAction.paginate))
async def peg_products(call: CallbackQuery, state: FSMContext, callback_data: SearchCallback):
    await call.answer()
    data = await state.get_data()
    products = await ProductsDAO.select_products_by_filter(**data)
    product = products[callback_data.page]

    await call.message.edit_media(InputMediaPhoto(
        media=SearchUtils.get_photo_products_by_id(product.photo),
        caption=SearchUtils.create_message_for_item_card( # type: ignore
        product # type: ignore
        ),),
        reply_markup=await get_search_peg_keyboard(
            len(products), # type: ignore
            callback_data.page))


@router.callback_query(StateFilter(ViewCatalog.view_introductory_page),
                       F.data == CatalogButtonFont.callback_search_by_name)
async def search_by_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.search_by_name)
    await call.message.answer(SearchFont.search_by_name,
                              reply_markup=reset_search)


@router.message(StateFilter(ViewCatalog.search_by_name),
                F.text.as_("name"))
async def get_name(message: Message, state: FSMContext, name: str):
    per_page = 0
    await state.set_state(ViewCatalog.view_items)
    products = await ProductsDAO.get_all_by_name(name)
    if not products:
        await message.answer(
        SearchUtils.create_message_for_item_card(None),
        reply_markup=await get_search_peg_keyboard(len(products), per_page)) # type: ignore
        return

    product = products[per_page]
    await message.answer_photo(
        caption=SearchUtils.create_message_for_item_card(product),
        photo=SearchUtils.get_photo_products_by_id(product.photo),
        reply_markup=await get_search_peg_keyboard(
            len(products), per_page))
