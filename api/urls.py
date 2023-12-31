from django.urls import path
from . import views

urlpatterns = [
    path('login', views.signin, name='login'),
    path('logout', views.logout, name="logout"),
    path('order_summary', views.OrderSummaryView.as_view(), name='order_summary'),
    path('order_summary/remove/<int:order_item_id>', views.RemoveOrderItemView.as_view(), name='remove_order_item'),
    path('order_summary/add/<int:order_item_id>', views.AddQuantityOrderItem.as_view(), name='add_quantity_order_item'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('order', views.order, name='order'),
    path('stats', views.stats, name='stats'),
    path('', views.product_list, name='product-list'),
    path('products/<int:pk>', views.view_product, name="product"),
    path('products/delete/<int:pk>', views.delete_product, name='delete_product'),
    path('products/edit/<int:pk>', views.edit_product, name='edit_product'),
    path('products/add/', views.add_product, name='add_product'),
]