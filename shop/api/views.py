from rest_framework import generics

from shop.models import Category, Product
from shop.api import serializers


class ProductList(generics.ListCreateAPIView):
    """
    An endpoint to create or retrieve all available products
    """

    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.filter(available=True)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint to retrieve, update, or delete product object
    """

    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'


class CategoryList(generics.ListCreateAPIView):
    """
    An endpoint to create or retrieve all categories
    """

    serializer_class = serializers.CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    An endpoint to retrieve, update, delete category object
    """

    serializer_class = serializers.CategoryProductSerializer
    queryset = Category.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'category_slug'
