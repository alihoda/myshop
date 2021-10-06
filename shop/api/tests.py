import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

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

    def _token_authentication(self, client: APIClient, user_obj: User) -> None:
        """
        Authenticate client with its token
        """
        token, created = Token.objects.get_or_create(user=user_obj)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_category_list(self):
        """
        Check retrieving all categories
        """
        url = reverse('shop:category_list')
        res = self.client.get(url)
        self.assertEqual(len(res.data), Category.objects.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_category_create(self):
        """
        Check creating category
        """
        url = reverse('shop:category_list')
        res = self.client.post(url, {'name': 'cat3'}, format='json')
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(pk=3).name, 'cat3')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_category_retrieve(self):
        """
        Check retrieving an existence category with its products
        """
        url = reverse('shop:category_detail', args=['cat1'])
        res = self.client.get(url)
        data = json.loads(res.content.decode())

        self.assertEqual(data['name'], 'cat1')
        self.assertEqual(
            len(data['products']), Category.objects.get(slug='cat1').products.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_category_update(self):
        """
        Check updating an existence category
        """
        url = reverse('shop:category_detail', args=['cat1'])
        res = self.client.put(url, {'name': 'c1'}, format='json')

        self.assertEqual(Category.objects.get(slug='c1').name, 'c1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_category_destory(self):
        """
        Check deleting an existence category
        """
        url = reverse('shop:category_detail', args=['cat1'])
        res = self.client.delete(url)

        self.assertNotIn(
            'cat1', Category.objects.values_list('name', flat=True))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
