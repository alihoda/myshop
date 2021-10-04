from rest_framework import generics

from shop.models import Category, Product
from shop.api import serializers


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
