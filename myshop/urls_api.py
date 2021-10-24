from rest_framework.routers import DefaultRouter

from cart.api.views import CartViewSet
from orders.api.views import OrderViewSet
from shop.api.views import CategoryViewSet, ProductViewSet
from payment.api.views import PaymentViewSet

router = DefaultRouter()
router.register('cart', CartViewSet, 'cart')
router.register('order', OrderViewSet, 'order')
router.register('product', ProductViewSet, 'product')
router.register('category', CategoryViewSet, 'category')
router.register('payment', PaymentViewSet, 'payment')

urlpatterns = router.urls
