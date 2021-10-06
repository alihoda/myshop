from django.urls import path

from users.api import views


app_name = 'users'
urlpatterns = [
    path('', views.UserList.as_view(), name='user_list'),
    path('profile/', views.UserDetail.as_view(), name='user_detail'),
]
