from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser

from users.api import serializers

User = get_user_model()


class UserList(generics.ListAPIView):
    """
    Endpoint retrieving all users if requested user is admin
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAdminUser, ]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint retrieve, update, or destroy user object
    """
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]
    parser_classes = [JSONParser, ]

    def get_object(self):
        return self.request.user
