from sqladmin import ModelView

from app.db import (
    Products,
    Users,
)


class ProductsView(ModelView, model=Products):
    column_list = [
        Products.name,
        Products.amount,
        Products.price,
    ] + [
        Products.order_product
    ]

    column_searchable_list = [
        Products.name,
        Products.brand,
        Products.id
    ]

    column_sortable_list = [
        Products.price,
        Products.amount
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
