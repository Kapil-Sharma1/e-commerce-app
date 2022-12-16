from rest_framework.serializers import(
    ModelSerializer,
    SlugRelatedField
)
from inventory.models import Category, Product


class CategorySerializer(ModelSerializer):
    """
    This serializer is responsible for the serialization
    and de-serialization for the category model records.
    """

    class Meta:
        model = Category
        exclude = ['id']


class ProductCreateUpdateSerializer(ModelSerializer):
    """
    This serializer is responsible for the de-serialization
    for the product model records.
    """
    category = SlugRelatedField(
        slug_field="uuid",
        queryset = Category.objects.all(),
        # many = True
    )

    class Meta:
        model = Product
        exclude = ['id']
        



class RetrieveListProductSerializer(ModelSerializer):
    """
    This serializer is responsible for serialization 
    for the product model records.
    """
    category = CategorySerializer()


    class Meta:
        model = Product
        exclude = ['id']