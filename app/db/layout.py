import math
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, func, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.utils.filetype import FileType

from app.db.database import Base


class Products(Base):
    photo = Column(FileType())
    name: Mapped[str]
    taste: Mapped[str]
    brand: Mapped[str]
    volume: Mapped[float]  # объем
    fortress: Mapped[float]  # крепость
    chill: Mapped[bool]  # холодок
    type_nicotine: Mapped[str] # тип никотина
    price: Mapped[float]
    amount: Mapped[int]

    order_product = relationship("OrdersProducts", back_populates="product")

    def __repr__(self) -> str:
        end_of_string = 10
        name_len = len(self.name)
        max_len = 15 if name_len <= end_of_string else math.floor(name_len / 2)
        correct_name = f"{self.name[:max_len].strip()}{"..." if max_len < end_of_string else ""}"
        return correct_name


class Users(Base):
    name: Mapped[str]
    status: Mapped[str|None]

    order = relationship("Orders", back_populates="user")

    def __repr__(self) -> str:
        end_of_string = 10
        name_len = len(self.name)
        max_len = 15 if name_len <= end_of_string else math.floor(name_len / 2)
        correct_name = f"{self.name[:max_len].strip()}{"..." if max_len < end_of_string else ""}"
        return correct_name


class Orders(Base):
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc),
        server_default=func.now()
    )
    status: Mapped[str] = mapped_column(default="pending")
    # paid -> created -> Completed 
    # (On Hold, Cancelled, Refunded, Fraud Detected)
    desc: Mapped[str|None]

    order_product = relationship("OrdersProducts", back_populates="order")
    user = relationship("Users", back_populates="order")

    def __repr__(self) -> str:
        return super().__repr__() + f"{self.id}"


class OrdersProducts(Base):
    __tablename__ = 'orders_products' # type: ignore

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    price_at_order: Mapped[float] # sum(product.price * product.amount) WHERE
                                  # order_id == {order_id} and product_id == product.id

    product = relationship("Products", back_populates="order_product")
    order = relationship("Orders", back_populates="order_product")

    def __repr__(self) -> str:
        return super().__repr__() + f"{self.id}"

