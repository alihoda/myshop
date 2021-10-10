from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.api.serializers import CartSerializer
from cart.cart import Cart
from shop.models import Product


class CartViewSet(viewsets.ViewSet):
    """
    Endpoint to retrieve, add, or remove a product to/from the cart.
    """
    permission_classes = [permissions.IsAuthenticated, ]

    @action(detail=False, methods=['get'])
    def detail(self, request):
        """
        Retrieve the cart.
        """
        cart = Cart(request.session)
        return Response(data=cart, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add(self, request, pk):
        """
        Add a product to the cart.
        """
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            product = get_object_or_404(Product, id=pk)
            cart = Cart(request.session)
            cart.add(
                product=product,
                quantity=serializer.data['quantity'],
                override_quantity=serializer.data['override_quantity']
            )
        return Response(f'{product.name} successfully added to the cart',
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove(self, request, pk):
        """
        Remove a product from the cart.
        """
        cart = Cart(request.session)
        product = get_object_or_404(Product, id=pk)
        cart.remove(product)
        return Response(f'{product.name} successfully removed from the cart', status=status.HTTP_200_OK)
