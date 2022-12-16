from django.urls import path

from inventory.views import CategoryViewset, ProductViewset

app_name = "inventory"

urlpatterns = [

    # |=============================== Category APIs ===========================| #
    path(
        route="category/",
        view=CategoryViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="category_list_create"
    ),
    path(
        route="category/<slug:uuid>",
        view=CategoryViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="category_retrieve_update_delete"
    ),

    # |=============================== Product APIs ===========================| #
    path(
        route="product/",
        view=ProductViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="product_list_create"
    ),
    path(
        route="product/<slug:uuid>",
        view=ProductViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="product_retrieve_update_delete"
    )
]