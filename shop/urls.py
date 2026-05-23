from django.contrib import admin
from django.urls import include, path
from shop.payment_views import create_test_checkout_session

app_name = 'shop'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('market.urls')),
    path('payment/<int:order_id>/', create_test_checkout_session, name='test_payment'),
]
