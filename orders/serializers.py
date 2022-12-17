from rest_framework.serializers import(
    ModelSerializer,
    SlugRelatedField,
    PrimaryKeyRelatedField
)

from django.contrib.auth.models import User
from inventory.models import Product
from orders.models import Cart, Order, OrderInfo
from inventory.serializers import RetrieveListProductSerializer


class CreateUpdateCartSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the Cart model records.
    """

    user = PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        # many = True
    )

    product = SlugRelatedField(
        slug_field="uuid",
        queryset = Product.objects.all(),
        # many = True
    )

    class Meta:
        model = Cart
        exclude = ['id']


class RetrieveListCartSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the Cart model records.
    """

    product = RetrieveListProductSerializer()
    

    class Meta:
        model = Cart
        exclude = ['id']



class OrderCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the order model records.
    """

    user = PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )

    class Meta:
        model = Order
        exclude = ['id']


class OrderRetrieveListSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the order model records.
    """

    class Meta:
        model = Order
        exclude = ['id']


class OrderInfoCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the orderinfo model records.
    """
    
    order = SlugRelatedField(
        slug_field="uuid",
        queryset = Order.objects.all()
    )

    product = SlugRelatedField(
        slug_field="uuid",
        queryset = Product.objects.all()
    )

    class Meta:
        model = OrderInfo
        exclude = ['id']



class OrderInfoRetrieveListSerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    for the orderinfo model records.
    """

    order = OrderRetrieveListSerializer()
    product = RetrieveListProductSerializer()


    class Meta:
        model = OrderInfo
        exclude = ['id']