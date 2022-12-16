from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel

from core.behaviours import UUIDMixin
from inventory.models import Product




class Cart(UUIDMixin, TimeStampedModel):

    """
    This model represent cart.
    """

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="cartproducts",
        related_query_name="cartproduct"
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name= "cart",
        related_query_name="cart"
    )


    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "cart"
        verbose_name = "cart"
        verbose_name_plural = "cart"

    def __repr__(self) -> str:
        return f"{self.product}: {self.user}"

    def __str__(self) -> str:
        return f"{self.product}: {self.user}"


class Order(UUIDMixin, TimeStampedModel):
    """
    This model represents Order
    """

    user = models.ForeignKey(
        to=User, 
        on_delete=models.CASCADE,
        related_name= "user_orders",
        related_query_name= "user_order"
    )
    class order_status_choice(models.TextChoices):
        IN_TRANSIT = ("TRANSIT","In Transit")
        DELIVERED = ("DELIVERED","Delivered")
        CANCELDED = ("CANCELLED","Cancelled")

    order_status = models.CharField(
        max_length=50,
        choices=order_status_choice.choices
    )

    class Meta:
        db_table = "Order"
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __repr__(self) -> str:
        return f'{self.user} : {self.order_status}'

    def __str__(self) -> str:
        return f'{self.user} : {self.order_status}'


class OrderInfo(UUIDMixin):
    """
    This model represents the details of that order.
    """

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="orderdetails",
        related_query_name="orderdetails"
    )

    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name="orderinfo",
        related_query_name="orderinfo"
    )

    total_cost = models.IntegerField(null=True, blank=True)

    quantity = models.IntegerField(default=1)


    class Meta:
        db_table = "OrderInfo"
        verbose_name = "OrderInfo"
        verbose_name_plural = "OrderInfo"

    def __repr__(self) -> str:
        return f'{self.order} : {self.product}: {self.total_cost}: {self.quantity}'

    def __str__(self) -> str:
        return f'{self.order} : {self.product}: {self.total_cost}: {self.quantity}'