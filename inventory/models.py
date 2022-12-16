from django.db import models

from core.behaviours import UUIDMixin


class Category(UUIDMixin):
    """
    This model represents category
    """

    name = models.CharField(max_length=50)


    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name



class Product(UUIDMixin):
    """
    This model represents product.
    A category can have many products.
    """
    name = models.CharField(max_length=50)
    cost = models.IntegerField()
    is_available  = models.BooleanField()

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name= "products",
        related_query_name= "product"
    )

    class Meta:
        db_table = "products"
        verbose_name = "product"
        verbose_name_plural = "products"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
