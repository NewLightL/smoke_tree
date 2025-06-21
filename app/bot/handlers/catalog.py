from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import app.bot.keyboars.base_keyboards as base_kb
from app.bot.fonts.button_font import StartButtonFont, CatalogButtonFont
from app.bot.fonts.message_font import CatalogFont
from app.bot.state.catalog_state import ViewCatalog

router = Router()


@router.callback_query(F.data == StartButtonFont.callback_catalog)
async def catalog_view(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_introductory_page)
    await call.answer()
    await call.message.edit_text(CatalogFont.introductory_page, # type: ignore
                                 reply_markup=base_kb.search_catalog)


@router.callback_query(F.data == CatalogButtonFont.callback_filter)
async def filter_view(call: CallbackQuery, state: FSMContext):
    await state.set_state(ViewCatalog.view_filters)
    await call.answer()
    await call.message.edit_text(CatalogFont.filters_page, # type: ignore
                                 reply_markup=base_kb.all_filters)
