from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, FSInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import app.bot.keyboars.base_keyboards as base_kb
from app.bot.callback.search_fabric import SearchAction, SearchCallback
from app.bot.keyboars.catalog_keyboards import get_peg_filter
from app.bot.fonts.button_font import BaseButtonFont, StartButtonFont, CatalogButtonFont, FiltersButtonFont
from app.bot.fonts.message_font import CatalogFont
from app.bot.fonts.call_font import CallAnswerFont
from app.bot.state.catalog_state import ViewCatalog
from app.bot.filters.catalog_filters import CorrectColumn
from app.bot.callback.catalog_fabric import Action, CallbackProduct
from app.bot.utils.catalog import CatalogUtils


router = Router()

@router.callback_query(F.data == StartButtonFont.callback_catalog)
async def catalog_view_answer(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_introductory_page)
    await state.set_data({})
    await call.answer()
    await call.message.edit_text(  # type: ignore
        CatalogFont.introductory_page,
        reply_markup=base_kb.search_catalog)


@router.callback_query(StateFilter(ViewCatalog.view_items),
                       SearchCallback.filter(F.action == SearchAction.home))
async def catalog_view_delete_last_mess(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_introductory_page)
    await state.set_data({})
    await call.answer()
    await call.bot.delete_message(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    await call.message.answer(  # type: ignore
        CatalogFont.introductory_page,
        reply_markup=base_kb.search_catalog)


@router.callback_query(StateFilter(ViewCatalog.view_items),
                       SearchCallback.filter(F.action == SearchAction.filter))
@router.callback_query(StateFilter(ViewCatalog.search_by_name,
                                   ViewCatalog.select_price),
                       F.data == BaseButtonFont.callback_reset)
async def filter_view_answer(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_filters)
    await call.answer()
    await call.bot.delete_message(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    await call.message.answer( # type: ignore
            CatalogFont.filters_page,
            reply_markup=base_kb.all_filters)


@router.callback_query(F.data == CatalogButtonFont.callback_filter,
                       StateFilter(ViewCatalog.view_introductory_page))
async def filter_view_edit(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_filters)
    await call.answer()
    await call.message.edit_text( # type: ignore
        CatalogFont.filters_page,
        reply_markup=base_kb.all_filters)


@router.callback_query(CorrectColumn(FiltersButtonFont.get_all_callback()),
                       StateFilter(ViewCatalog.view_filters),
                       F.data.as_("name_column"))
async def handle_filters(call: CallbackQuery, state: FSMContext, name_column: str):
    await call.answer()
    await state.set_state(ViewCatalog.view_filter_parametr)
    data = await state.get_data()
    await call.message.edit_text(text=CatalogFont.filter_page,  # type: ignore
                                 reply_markup=await get_peg_filter(name_column, data))


@router.callback_query(CallbackProduct.filter(F.action==Action.select),
                       StateFilter(ViewCatalog.view_filter_parametr))
async def click_on_parametr(call: CallbackQuery, callback_data: CallbackProduct,
                            state: FSMContext):
    await call.answer()
    key, value = CatalogUtils.get_correct_variable(callback_data.pack())
    if await state.get_value(callback_data.filter_type) == value:  # type: ignore
        data = await state.get_data()
        del data[callback_data.filter_type]  # type: ignore
        await state.set_data(data)
    else:
        if key == "value_bool":
            value = bool(value)
        await state.update_data({callback_data.filter_type: value})  # type: ignore

    data = await state.get_data()
    await call.message.edit_text(text=CatalogFont.filter_page,  # type: ignore
                                 reply_markup=await get_peg_filter(
                                     callback_data.filter_type,  # type: ignore
                                     data,
                                     callback_data.page))


@router.callback_query(F.data == FiltersButtonFont.callback_price,
                       StateFilter(ViewCatalog.view_filters))
async def write_price_for_item(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.select_price)
    data = await state.get_data()
    price = data.get("price", None)
    await call.message.edit_text(  # type: ignore
        text=CatalogFont.user_price(price),
        reply_markup=base_kb.reset_search
        )


@router.message(~F.text.isdigit(),
                StateFilter(ViewCatalog.select_price))
async def not_correct_price_for_item(mess: Message):
    await mess.answer(text=CatalogFont.not_correct_price)  # type: ignore


@router.message(F.text.isdigit(),
                StateFilter(ViewCatalog.select_price),
                F.text.as_("price"))
async def correct_price_for_item(mess: Message, state: FSMContext, price: int):
    await state.update_data({"price": price})
    await state.set_state(ViewCatalog.view_filters)
    await mess.answer(text=CatalogFont.end_of_select_price)
    await mess.answer(CatalogFont.filters_page,
                    reply_markup=base_kb.all_filters)


@router.callback_query(StateFilter(ViewCatalog.view_filter_parametr),
                       CallbackProduct.filter(F.action == Action.reset))
async def reset_one_filter(call: CallbackQuery, state: FSMContext,
                           callback_data: CallbackProduct):
    await call.answer(CallAnswerFont.reset)
    data = await state.get_data()
    return_value = data.get(callback_data.filter_type)  # type: ignore
    if return_value is None:  # type: ignore
        return
    del data[callback_data.filter_type]  # type: ignore
    await state.set_data(data)
    await call.message.edit_text(text=CatalogFont.filter_page,  # type: ignore
                                 reply_markup=await get_peg_filter(
                                     callback_data.filter_type,  # type: ignore
                                     data,
                                     callback_data.page))


@router.callback_query(StateFilter(ViewCatalog.view_filters),
                       F.data == BaseButtonFont.callback_reset)
async def reset_all_filters(call: CallbackQuery, state: FSMContext):
    await call.answer(CallAnswerFont.reset)
    data = await state.get_data()
    if not data:
        return
    await state.set_data({})


@router.callback_query(StateFilter(ViewCatalog.view_filter_parametr),
                       CallbackProduct.filter(F.action == Action.paginate))
async def change_page_filter_parametr(call: CallbackQuery, state: FSMContext,
                                    callback_data: CallbackProduct):
    await call.answer()
    data = await state.get_data()
    await call.message.edit_text(text=CatalogFont.filters_page,  # type: ignore
                                 reply_markup=await get_peg_filter(
                                     callback_data.filter_type,  # type: ignore
                                     data,
                                     callback_data.page
                                 ))


@router.callback_query(StateFilter(ViewCatalog.view_filter_parametr),
                       CallbackProduct.filter(F.action == Action.apply))
async def apply_filter_parametr(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.view_filters)
    await call.message.edit_text(CatalogFont.filters_page,  # type: ignore
                                 reply_markup=base_kb.all_filters)
