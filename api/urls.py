from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('products/', views.getProducts, name='products'),
    path('orders/', views.getOrders, name="orders"),
    path('orders/items', views.getOrdersItem, name="ordersItem"),
]