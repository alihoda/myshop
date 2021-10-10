from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from cart.api.views import CartViewSet


app_name = 'cart'

router = DefaultRouter()
router.register('cart', CartViewSet, basename='cart')
urlpatterns = router.urls
