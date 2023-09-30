from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list, name='listOfProducts'),
    # path('', views.index, name='index'),
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    # path('products/<int:pk>/edit/', views.EditProductView.as_view(), name='edit_product'),
    path('products/add/', views.add_product, name='add_product'),
    path('orders/', views.getOrders, name="orders"),
    path('orders/items', views.getOrdersItem, name="ordersItem"),
]