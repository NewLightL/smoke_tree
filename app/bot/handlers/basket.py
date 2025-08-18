from pydantic import TypeAdapter

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from app.bot.callback.basket_fabric import BasketAction, BasketCallback
from app.bot.callback.search_fabric import SearchAction, SearchCallback
from app.bot.fonts.button_font import StartButtonFont
from app.bot.fonts.call_font import CallAnswerFont
from app.bot.fonts.message_font import BasketFont
from app.bot.state.catalog_state import ViewCatalog
from app.bot.utils.basket import BasketUtils
from app.bot.utils.search import SearchUtils
from app.bot.keyboars.basket_keyboards import create_peg_basket, order_keyboards
from app.core import load_config
from app.db import Products, ProductsDAO


router = Router()

settings = load_config()


@router.callback_query(F.data == StartButtonFont.callback_basket)
async def get_basket(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.view_basket)
    basket_str: str|None = await state.get_value("basket", {})

    if basket_str is None or not basket_str:
        await call.message.edit_text(  # type: ignore
        text=BasketFont.basket_is_empty,
        reply_markup=await create_peg_basket(0)
        )
        return

    basket = TypeAdapter(dict[int, int]).validate_python(basket_str)

    ids = TypeAdapter(list[int]).validate_python(basket.keys())
    products_basket = await ProductsDAO.get_all_by_id(ids)
    if products_basket is None or not products_basket:
        await call.message.edit_text(  # type: ignore
        text=BasketFont.basket_is_empty,
        reply_markup=await create_peg_basket(0)
        )
        return

    product: Products = products_basket[0]
    await call.message.edit_media(
        InputMediaPhoto(
            media=SearchUtils.get_photo_products_by_id(product.photo),
            caption=SearchUtils.create_message_for_item_card(product)
        ),
        reply_markup=await create_peg_basket(
            len(products_basket),
            product.id,
            0,
            basket[product.id],
            product.amount
        )
    )


@router.callback_query(StateFilter(ViewCatalog.view_items),
                       SearchCallback.filter(F.action == SearchAction.basket))
@router.callback_query(StateFilter(ViewCatalog.create_order),
                       F.data == StartButtonFont.callback_basket)
async def get_basket_delete(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.view_basket)
    await call.bot.delete_message(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)
    basket_str: str|None = await state.get_value("basket", {})

    if basket_str is None or not basket_str:
        await call.message.answer(  # type: ignore
        text=BasketFont.basket_is_empty,
        reply_markup=await create_peg_basket(0)
        )
        return

    basket = TypeAdapter(dict[int, int]).validate_python(basket_str)

    ids = TypeAdapter(list[int]).validate_python(basket.keys())
    products_basket = await ProductsDAO.get_all_by_id(ids)
    if products_basket is None or not products_basket:
        await call.message.answer(  # type: ignore
        text=BasketFont.basket_is_empty,
        reply_markup=await create_peg_basket(0)
        )
        return

    product: Products = products_basket[0]
    await call.message.answer_photo(
        photo=SearchUtils.get_photo_products_by_id(product.photo),
        caption=SearchUtils.create_message_for_item_card(product),
        reply_markup=await create_peg_basket(
            len(products_basket),
            product.id,
            0,
            basket[product.id],
            product.amount
        )
    )


@router.callback_query(StateFilter(ViewCatalog.view_basket),
                       BasketCallback.filter(F.action == BasketAction.paginate))
async def paginate_basket(call: CallbackQuery, state: FSMContext, callback_data: BasketCallback):
    basket_str: str|None = await state.get_value("basket")
    basket = TypeAdapter(dict[int, int]).validate_python(basket_str)

    ids = TypeAdapter(list[int]).validate_python(basket.keys())
    products_basket = await ProductsDAO.get_all_by_id(ids)
    product: Products = products_basket[callback_data.page]

    await call.message.edit_media(InputMediaPhoto(
        media=SearchUtils.get_photo_products_by_id(product.photo),
        caption=SearchUtils.create_message_for_item_card( # type: ignore
        product # type: ignore
        ),),
        reply_markup=await create_peg_basket(
            len(products_basket), # type: ignore
            product.id,
            callback_data.page,
            basket[product.id],
            product.amount))


@router.callback_query(StateFilter(ViewCatalog.view_basket),
                       BasketCallback.filter(F.action == BasketAction.reset))
async def reset_basket(call: CallbackQuery, state: FSMContext):
    await call.answer(CallAnswerFont.basket_reset)
    await state.update_data({"basket": {} })
    await call.bot.delete_message(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id)

    await call.message.answer(  # type: ignore
        text=BasketFont.basket_is_empty,
        reply_markup=await create_peg_basket(0)
        )

@router.callback_query(StateFilter(ViewCatalog.view_basket),
                       BasketCallback.filter(F.action == BasketAction.plus))
async def plus_products_in_basket(call: CallbackQuery,
                                  state: FSMContext,
                                  callback_data: BasketCallback):
    await call.answer(CallAnswerFont.plus_product)
    basket: dict[int, int] = TypeAdapter(dict[int, int]).validate_python(await state.get_value("basket"))
    basket[callback_data.product_id] = callback_data.count
    await state.update_data({"basket": basket})

    ids = TypeAdapter(list[int]).validate_python(basket.keys())
    products_basket = await ProductsDAO.get_all_by_id(ids)
    product: Products = products_basket[callback_data.page]

    await call.message.edit_media(InputMediaPhoto(
        media=SearchUtils.get_photo_products_by_id(product.photo),
        caption=SearchUtils.create_message_for_item_card( # type: ignore
        product # type: ignore
        ),),
        reply_markup=await create_peg_basket(
            len(products_basket), # type: ignore
            product.id,
            callback_data.page,
            basket[product.id],
            product.amount))


@router.callback_query(StateFilter(ViewCatalog.view_basket),
                       BasketCallback.filter(F.action == BasketAction.minus))
async def minus_products_in_basket(call: CallbackQuery,
                                  state: FSMContext,
                                  callback_data: BasketCallback):
    await call.answer(CallAnswerFont.minus_product)
    basket: dict[int, int] = TypeAdapter(dict[int, int]).validate_python(await state.get_value("basket"))
    basket[callback_data.product_id] = callback_data.count
    await state.update_data({"basket": basket})

    ids = TypeAdapter(list[int]).validate_python(basket.keys())
    products_basket = await ProductsDAO.get_all_by_id(ids)
    product: Products = products_basket[callback_data.page]

    await call.message.edit_media(InputMediaPhoto(
        media=SearchUtils.get_photo_products_by_id(product.photo),
        caption=SearchUtils.create_message_for_item_card( # type: ignore
        product # type: ignore
        ),),
        reply_markup=await create_peg_basket(
            len(products_basket), # type: ignore
            product.id,
            callback_data.page,
            basket[product.id],
            product.amount))


@router.callback_query(StateFilter(ViewCatalog.view_basket),
                       BasketCallback.filter(F.action == BasketAction.confirm))
async def minus_products_in_basket(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ViewCatalog.create_order)
    basket: dict[int, int] = TypeAdapter(dict[int, int]).validate_python(await state.get_value("basket"))

    await call.bot.delete_message(chat_id=call.message.chat.id,
                                message_id=call.message.message_id)

    await call.message.answer(
        text=await BasketUtils.get_card_basket(basket),
        reply_markup=order_keyboards
    )
