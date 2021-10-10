from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken import views

from cart.api.urls import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.api.urls', namespace='shop')),
    path('users/', include('users.api.urls', namespace='users')),
    path('', include('cart.api.urls', namespace='cart')),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
