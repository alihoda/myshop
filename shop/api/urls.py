from django.urls import path

from shop.api import views


app_name = 'shop'

urlpatterns = [
    path('category/', views.CategoryList.as_view(), name='category_list'),
    path('category/<slug:category_slug>/',
         views.CategoryDetail.as_view(), name='category_detail'),
    path('', views.ProductList.as_view(), name='product_list'),
    path('product/<slug:product_slug>/',
         views.ProductDetail.as_view(), name='product_detail'),
]
