from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework.authtoken.models import Token

from cart.cart import Cart
from shop.models import Product
from orders.models import Order, OrderItem


User = get_user_model()


class OrderTest(APITestCase):
    def setUp(self) -> None:
        self.prod1 = Product.objects.create(name='Product1', price=99.10)
        self.prod2 = Product.objects.create(name='Product2', price=100.10)
        self.user = User.objects.create_user('test', 'test@mail.com', '1234')
        self._token_authentication(self.client, self.user)
        # self.cart = Cart(self.client.session)
        # self.cart.add(self.prod1, 2)

    def _token_authentication(self, client: APIClient, user_obj: User) -> None:
        """
        Authenticate client with its token
        """
        token, created = Token.objects.get_or_create(user=user_obj)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_order_create(self):
        """
        Ensure can create order.
        """
        url = reverse('api:cart-add', args=[self.prod1.id])
        self.client.post(url, {'quantity': 5})
        data = {'first_name': 'first', 'last_name': 'last', 'email': 'test@mail.com',
                'address': 'Isfahan, Iran', 'city': 'Isfahan', 'postal_code': '1111111'}
        url = reverse('api:order-list')
        res = self.client.post(url, data)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
