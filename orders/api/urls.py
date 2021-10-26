from django.urls import path

from orders.views import admin_order_detail


app_name = 'orders'
urlpatterns = [
    path('admin/order/<int:order_id>/',
         admin_order_detail, name='admin_order_detail')
]
