from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from shop.models import Category, Product


User = get_user_model()


class CategoryTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@mail.com', '1234')
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@mail.com', '1234')
        cat1 = Category.objects.create(name='cat1')
        cat2 = Category.objects.create(name='cat2')
        prod1 = Product.objects.create(name='Product1', price=99.10)
        prod2 = Product.objects.create(name='Product2', price=100.10)
        cat1.products.add(prod1, prod2)
        cat2.products.add(prod2)

    def test_category_list(self):
        """
        Check retrieving all categories
        """
        url = reverse('shop:category_list')
        res = self.client.get(url)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
