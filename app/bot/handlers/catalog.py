from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import app.bot.keyboars.base_keyboards as base_kb
from app.bot.keyboars.catalog_keyboards import get_peg_filter
from app.bot.fonts.button_font import StartButtonFont, CatalogButtonFont, FiltersButtonFont
from app.bot.fonts.message_font import CatalogFont
from app.bot.state.catalog_state import ViewCatalog
from app.bot.filters.catalog_filters import CorrectColumn
from app.bot.callback.catalog_fabric import Action, CallbackProduct


router = Router()


@router.callback_query(F.data == StartButtonFont.callback_catalog)
async def catalog_view(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_introductory_page)
    await call.answer()
    await call.message.edit_text(CatalogFont.introductory_page, # type: ignore
                                 reply_markup=base_kb.search_catalog)


@router.callback_query(F.data == CatalogButtonFont.callback_filter,
                       StateFilter(ViewCatalog.view_introductory_page))
async def filter_view(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_filters)
    await call.answer()
    await call.message.edit_text(CatalogFont.filters_page, # type: ignore
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

    if await state.get_value(callback_data.filter_type) == callback_data.value:  # type: ignore
        data = await state.get_data()
        if not data.get(callback_data.filter_type):  # type: ignore
            return
        del data[callback_data.filter_type]  # type: ignore
        await state.set_data(data)
    else:
        # TODOs Привести к изначальному типу
        await state.update_data({callback_data.filter_type: callback_data.value})  # type: ignore


    data = await state.get_data()
    await call.message.edit_text(text=CatalogFont.filter_page,  # type: ignore
                                 reply_markup=await get_peg_filter(
                                     callback_data.filter_type,  # type: ignore
                                     data,
                                     callback_data.page))


@router.callback_query(StateFilter(ViewCatalog.view_filter_parametr),
                       CallbackProduct.filter(F.action == Action.reset))
async def reset_one_filter(call: CallbackQuery, state: FSMContext,
                           callback_data: CallbackProduct):
    await call.answer()
    data = await state.get_data()
    if not data.get(callback_data.filter_type):  # type: ignore
        return
    del data[callback_data.filter_type]  # type: ignore
    await state.set_data(data)
    await call.message.edit_text(text=CatalogFont.filter_page,  # type: ignore
                                 reply_markup=await get_peg_filter(
                                     callback_data.filter_type,  # type: ignore
                                     data,
                                     callback_data.page))


@router.callback_query(StateFilter(ViewCatalog.view_filters),
                       CallbackProduct.filter(F.action == Action.reset))
async def reset_all_filters(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.edit_text(text=CatalogFont.filters_page,  # type: ignore
                                 reply_markup=base_kb.all_filters)


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
    await call.message.edit_text(CatalogFont.filters_page,
                                 reply_markup=base_kb.all_filters)
    print(await state.get_data())
