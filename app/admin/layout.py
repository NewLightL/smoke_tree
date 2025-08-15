from sqladmin import ModelView

from app.db import (
    Products,
    Users,
    Orders,
    OrdersProducts
)


class ProductsView(ModelView, model=Products):
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-solid fa-cart-shopping"

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

    column_labels = {
        Products.name: "Название",
        Products.amount: "Количество",
        Products.price: "Цена",
        Products.order_product: "Заказ_Товар"
    }


class UsersView(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"

    can_delete = False

    column_list = [
        Users.name,
        Users.status,
    ] + [
        Users.order
    ]

    column_searchable_list = [
        Users.name,
        Users.status,
    ]

    column_labels = {
        Users.name: "Название",
        Users.status: "Статус",
        Users.order: "Заказ"
    }


class OrdersView(ModelView, model=Orders):
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-solid fa-box"

    column_list = [
        Orders.status,
        Orders.created_at,
        Orders.desc,
    ] + [
        Orders.user,
        Orders.order_product
    ]

    column_searchable_list = [
        Orders.status,
        Orders.created_at,
        Orders.user
    ]

    column_sortable_list = [
        Orders.created_at
    ]

    column_formatters = {
        Orders.created_at: lambda m, a: m.created_at.strftime("%d-%m-%Y"),
        Orders.desc: lambda m, a: ("" if m.desc is None else
                                   (m.desc[:10] + "..."
                                   if len(m.desc) > 10 else
                                   m.desc))
    }

    column_labels = {
        Orders.status: "Статус",
        Orders.created_at: "Создан",
        Orders.desc: "Описание",
        Orders.user: "Пользователь",
        Orders.order_product: "Заказ_Товар",
    }


class OrdersProductsView(ModelView, model=OrdersProducts):
    name = "Заказ_Товар"
    name_plural = "Заказы_Товары"
    icon = "fa-solid fa-cart-shopping"

    column_list = [
        OrdersProducts.quantity,
        OrdersProducts.price_at_order
    ] + [
        OrdersProducts.order,
        OrdersProducts.product
    ]

    column_searchable_list = [
        OrdersProducts.product,
        OrdersProducts.order
    ]

    column_labels = {
        OrdersProducts.quantity: "Количество",
        OrdersProducts.price_at_order: "Цена заказа",
        OrdersProducts.order: "Заказ",
        OrdersProducts.product: "Товар",
    }
