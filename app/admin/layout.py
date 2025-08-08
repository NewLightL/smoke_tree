from sqladmin import ModelView

from app.db import (
    Products,
    Users,
    Orders,
    OrdersProducts
)


class ProductsView(ModelView, model=Products):
    column_list = [
        Products.name,
        Products.amount,
        Products.price,
    ] + [
        Products.order_product
    ]

    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-cart-shopping"


class UsersView(ModelView, model=Users):
    column_list = [
        Users.name,
        Users.status,
    ] + [
        Users.order
    ]

    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class OrdersView(ModelView, model=Orders):
    column_list = [
        Orders.status,
        Orders.desc,
        Orders.created_at
    ] + [
        Orders.order_product,
        Orders.user
    ]

    column_formatters = {Orders.desc: lambda m, a: m.desc[:15] if m.desc is not None else ""}
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-truck"


class OrdersProductsView(ModelView, model=OrdersProducts):
    column_list = [
        OrdersProducts.quantity,
        OrdersProducts.price_at_order,
    ] + [
        OrdersProducts.product,
        OrdersProducts.order
    ]

    name = "Заказ_товар"
    name_plural = "Заказы_Товары"
    icon = "fa-solid fa-book"
    
