from django.urls import path
from . import views

app_name = 'market'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-complete/<int:order_id>/', views.order_complete, name='order_complete'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
