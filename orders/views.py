from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from orders.models import Cart, Order, OrderInfo
from orders.serializers import(
    RetrieveListCartSerializer,
    OrderCreateUpdateSerializer,
    OrderRetrieveListSerializer,
    OrderInfoCreateUpdateSerializer,
    OrderInfoRetrieveListSerializer
)
from orders.pagination import OrderPagination
from inventory.models import Product
from core.renderers import CustomRenderer


class CartViewset(GenericViewSet):

    # Auth
    permission_classes = [IsAuthenticated]

    
#  /============================ API to add product in cart ===================/  #      


    def add_product(self, request, *args, **kwargs):
        """
        This API is used to add a product in the user's cart 
        or change it's quantity if the product is already added in the cart.
        """
        # Fetching the user
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Fetching the product
        product_uuid = kwargs.get('product_uuid')
        product = Product.objects.get(
            uuid = product_uuid,
            is_available = True
        )

        # fetching the quantity
        quantity = int(request.data.get('quantity'))

        # Checks if the product is already present in the user's cart
        cart_product = Cart.objects.filter(
            user = user,
            product = product,
        ).first()
        # If the product is not present in the cart add a record for the product
        if not cart_product:
            cart_product = Cart.objects.create(
                user = user,
                product = product,
                quantity = quantity
            )
        else:
            cart_product.quantity = quantity

        response = {
            "data": {
                "user": cart_product.user.id,
                "product": cart_product.product.uuid,
                "quantity": quantity
            }
        }

        return Response(
            data = response, 
            status = status.HTTP_202_ACCEPTED
        )     

#  /============================ API to remove product from cart ====================/  #

    def remove_product(self, request, *args, **kwargs):
        """
        This API is used to remove product(s) from the user's cart.
        We cannot change the quantity in this API as user will have 
        to empty its cart then make a order from scratch.
        """

        # Fetching the user
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)

        # Fetching the product
        product_uuid = kwargs.get('product_uuid')
        product = Product.objects.get(uuid = product_uuid)

        
        # Checks if the product is already present in the user's cart
        my_cart = Cart.objects.filter(
            user = user,
            product = product
        ).first()

        if not my_cart:
            return Response(
                data={
                    'message' : 'cart is empty'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        # deleting the cart
        my_cart.delete()

        return Response(
            data={
                "message": 'product removed from cart'
            },
            status=status.HTTP_202_ACCEPTED
        )



# /============================== Orders API's ==========================/ #

class OrderViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    
    permission_classes = [IsAuthenticated]
    serializer_class = OrderRetrieveListSerializer
    pagination_class = OrderPagination
    renderer_classes = [CustomRenderer]

    action_permissions = {
        "list": [ IsAuthenticated, IsAdminUser ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated],
        "destroy": [ IsAuthenticated],
        "create": [ IsAuthenticated]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
    

  
    

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of order records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested order record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested order record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested order record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New order record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        order = get_object_or_404(
            Order, 
            uuid = self.kwargs.get("uuid")
        )
        return order

    def get_queryset(self, *args, **kwargs):
        queryset = Order.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderCreateUpdateSerializer
        else:
            return OrderRetrieveListSerializer

   

    def get_renderer_context(self):
        context = super().get_renderer_context()
        if self.action in self.response_data:
            context["message"] = (
                self.response_data.get(self.action).get("message")
            )
            context["status_code"] = (
                self.response_data.get(self.action).get("status_code")
            )
        return context


# /============================== OrderInfo API's ==========================/ #

class OrderInfoViewset(GenericViewSet):

    permission_classes = [IsAuthenticated]



    def add_orderdetails(self, request, *args, **kwargs):
        """
        This API is used to add the order details.
        """
        

        #fetching the order
        order_uuid = kwargs.get("order_uuid")
        order = Order.objects.get(uuid = order_uuid)

        #fetching the product
        product_uuid = kwargs.get("product_uuid")
        product = Product.objects.get(uuid = product_uuid)

        
        #fetching the quantity
        quantity = int(request.data.get("quantity"))

        total_cost = product.cost * quantity

        
       
        add_details = OrderInfo.objects.create(
            order = order,
            product = product,
            total_cost = total_cost,
            quantity = quantity
        )

        response = {
            "data" : {
                "order" : add_details.order.uuid,
                "product" : add_details.product.uuid,
                "total_cost" : total_cost,
                "quantity" : quantity
            }
        }

        return Response(
            data = response, 
            status = status.HTTP_202_ACCEPTED
        ) 

    
    
    
    def get_orderdetails(self, request, *args, **kwargs):
        """
        This API is to view the details of user' order
        """
        #fetching the details
        orderinfo = OrderInfo.objects.all()


        serialized_data = OrderInfoRetrieveListSerializer(
            instance=orderinfo,
            many = True
        ).data

        return Response(
            data={
                "message" : "requested details provided",
                "data" : serialized_data
            },
            status=status.HTTP_200_OK
        )







      