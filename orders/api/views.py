from rest_framework import status, viewsets
from rest_framework.response import Response

from cart.cart import Cart
from orders.api.serializers import OrderSerializer, OrderItemSerializer
from orders.models import Order, OrderItem
from orders.tasks import order_created


class OrderViewSet(viewsets.ModelViewSet):
    """
    Endpoint to list, retrieve, create, update, or delete order.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        cart = Cart(self.request.session)
        for item in cart:
            OrderItem.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])

        cart.clear()
        order_created.delay(order.id)
        self.request.session['order_id'] = order.id
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
