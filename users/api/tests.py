import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class UserTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            'test1', 'test1@mail.com', '1234')
        self.user2 = User.objects.create_user(
            'test2', 'test2@mail.com', '1234')
        self.superuser = User.objects.create_superuser(
            'admin', 'admin@mail.com', '1234')

    def _token_authentication(self, client: APIClient, user_obj: User) -> None:
        """
        Authenticate client with its token
        """
        token, created = Token.objects.get_or_create(user=user_obj)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_user_list_successful(self):
        """
        Ensure user's list retrieved successfully only by admin access
        """
        url = reverse('users:user_list')
        self._token_authentication(self.client, self.superuser)
        res = self.client.get(url)
        data = json.loads(res.content.decode())

        self.assertEqual(len(data), User.objects.count())
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_list_failed(self):
        """
        Ensure not admin user can not retrieve user's list
        """
        url = reverse('users:user_list')
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_retrieve(self):
        """
        Ensure user's profile retrieve successfully
        """
        url = reverse('users:user_detail')
        self._token_authentication(self.client, self.user1)
        res = self.client.get(url)
        data = json.loads(res.content.decode())

        self.assertEqual(data['username'], 'test1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_update(self):
        """
        Ensure user can update successfully
        """
        url = reverse('users:user_detail')
        self._token_authentication(self.client, self.user1)
        res = self.client.put(url, {'username': 'user1'}, format='json')
        user = User.objects.get(pk=1)

        self.assertEqual(user.username, 'user1')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_delete(self):
        """
        Ensure user can delete profile
        """
        url = reverse('users:user_detail')
        self._token_authentication(self.client, self.user1)
        res = self.client.delete(url)

        self.assertNotIn(
            'test1', User.objects.values_list('username', flat=True))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
