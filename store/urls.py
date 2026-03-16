from django.urls import path
from . import views

urlpatterns = [
    # product urls
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # search url
    path('search/', views.search, name='search'),

    # cart urls
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:id>/', views.update_cart, name='update_cart'),

    # checkout urls
    path('checkout/', views.checkout, name='checkout'),
    path('order/success/', views.order_success, name='order_success'),

    # order history urls
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:id>/', views.order_detail, name='order_detail'),
]