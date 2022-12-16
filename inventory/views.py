from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin,
    RetrieveModelMixin, UpdateModelMixin
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from django.shortcuts import get_object_or_404

from inventory.models import Category, Product
from core.renderers import CustomRenderer
from inventory.pagination import InventoryPagination
from inventory.serializers import(
    CategorySerializer,
    ProductCreateUpdateSerializer,
    RetrieveListProductSerializer
)


# /============================== Category API's ==========================/ #

class CategoryViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = InventoryPagination
    renderer_classes = [CustomRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    
    action_permissions = {
        "list": [ IsAuthenticated ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated, IsAdminUser],
        "destroy": [ IsAuthenticated, IsAdminUser],
        "create": [ IsAuthenticated, IsAdminUser]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
    

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of category records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested category record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested category record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested category record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New category record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        category = get_object_or_404(
            Category, 
            uuid = self.kwargs.get("uuid")
        )
        return category


    def get_queryset(self, *args, **kwargs):
        queryset = Category.objects.all()
        return queryset



    def get_serializer_class(self):
        return CategorySerializer

   

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


# /============================== Product API's ==========================/ #

class ProductViewset(
    ListModelMixin, CreateModelMixin, RetrieveModelMixin,
    UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    
    permission_classes = [IsAuthenticated]
    serializer_class = RetrieveListProductSerializer
    pagination_class = InventoryPagination
    renderer_classes = [CustomRenderer]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']



    action_permissions = {
        "list": [ IsAuthenticated ],
        "retrieve": [ IsAuthenticated ],
        "partial_update": [ IsAuthenticated, IsAdminUser],
        "destroy": [ IsAuthenticated, IsAdminUser],
        "create": [ IsAuthenticated, IsAdminUser]
    }

    def get_permissions(self):
        self.permission_classes = self.action_permissions[self.action] 
        return super().get_permissions()
    
     

    # The message that will be added in the response for each action in the
    # Viewset
    response_data = {
        "list": {
            "message": "List of product records",
            "status_code": status.HTTP_200_OK
        },
        "retrieve": {
            "message": "Requested product record retrieved",
            "status_code": status.HTTP_200_OK
        },
        "partial_update": {
            "message": "Requested product record updated",
            "status_code": status.HTTP_202_ACCEPTED
        },
        "destroy": {
            "message": "Requested product record deleted",
            "status_code": status.HTTP_204_NO_CONTENT
        },
        "create": {
            "message": "New product record created",
            "status_code": status.HTTP_201_CREATED
        }
    }

    def get_object(self):
        product = get_object_or_404(
            Product, 
            uuid = self.kwargs.get("uuid")
        )
        return product

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ProductCreateUpdateSerializer
        else:
            return RetrieveListProductSerializer

   

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

