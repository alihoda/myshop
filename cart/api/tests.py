import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from cart.cart import Cart
from shop.models import Product


User = get_user_model()


class CartTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@mail.com', '1234')
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@mail.com', '1234')
        self.prod1 = Product.objects.create(name='Product1', price=99.10)
        self.prod2 = Product.objects.create(name='Product2', price=100.10)

    def _token_authentication(self, client: APIClient, user_obj: User) -> None:
        """
        Authenticate client with its token
        """
        token, created = Token.objects.get_or_create(user=user_obj)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_cart_retrieve(self):
        """
        Ensure the cart can be retrieved.
        """
        self._token_authentication(self.client, self.user)

        cart = Cart(self.client.session)
        cart.add(self.prod1)
        cart.add(self.prod2, 5)

        url = reverse('cart:cart-items')
        res = self.client.get(url)
        data = json.loads(res.content.decode())

        self.assertEqual(len(data), len(cart))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cart_add(self):
        """
        Ensure a product can be added to the cart.
        """
        self._token_authentication(self.client, self.user)

        url = reverse('cart:cart-add', args=[self.prod1.id])
        res = self.client.post(url, {'quantity': 4})
        cart = self.client.session.get(settings.CART_SESSION_ID)

        self.assertIn(str(self.prod1.id), cart)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_cart_remove(self):
        """
        Ensure a product can be removed from the cart.
        """
        self._token_authentication(self.client, self.user)

        cart = Cart(self.client.session)
        cart.add(self.prod1)

        url = reverse('cart:cart-remove', args=[self.prod1.id])
        res = self.client.post(url)
        cart = self.client.session.get(settings.CART_SESSION_ID)

        self.assertNotIn(str(self.prod1.id), cart)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
