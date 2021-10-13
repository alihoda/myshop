from rest_framework import viewsets

from shop.models import Category, Product
from shop.api.serializers import ProductSerializer, CategoryProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Endpoint list, retrieve, create, update, or destory product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Endpoint list, retrieve, create, update, or destory category.
    """
    queryset = Category.objects.all()
    serializer_class = CategoryProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
