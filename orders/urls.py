from django.urls import path

from orders.views import CartViewset, OrderViewset, OrderInfoViewset

app_name = "orders"


# |=============================== Cart APIs ===========================| #


urlpatterns = [
    path(
        route='user/<int:user_id>/cart/product/<slug:product_uuid>/',
        view=CartViewset.as_view({
            'post' : 'add_product',
            'delete' : 'remove_product',
            
            
        })
    ),

  

    # |=============================== Orders APIs ===========================| #
    path(
        route="order/",
        view=OrderViewset.as_view({
            "get": "list",
            "post": "create"
        }),
        name="order_list_create"
    ),
    path(
        route="order/<slug:uuid>",
        view=OrderViewset.as_view({
            "get": "retrieve",
            "patch": "partial_update",
            "delete": "destroy"
        }),
        name="order_retrieve_update_delete"
    ),

    # |=============================== OrderInfo APIs ===========================| #
    path(
        route="orderinfo/order/<slug:order_uuid>/product/<slug:product_uuid>/",
        view=OrderInfoViewset.as_view({
            "post": "add_orderdetails"
        }),
        name="orderinfo_create"
    ),

    path(
        route="orderinfo/details/",
        view=OrderInfoViewset.as_view({
            "get" : "get_orderdetails"
        }),
        name="orderinfo_get"
    ),

    
]