from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.shop, name="shop"),
    path('product/<product_id>/', views.product, name="product"),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('cart/', views.carting.as_view(), name='cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('ordered/', views.success, name="success")
]