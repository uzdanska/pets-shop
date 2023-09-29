from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'quantity', 'order', 'products']
    # ['id', 'quantity', 'order', 'products']
    products = serializers.SerializerMethodField()
    def get_products(self, obj):
        products = {
            'name': obj.product.name,
            'category': obj.product.category.name,
            'description': obj.product.descrption,
            'price': obj.product.price
        }
        return products

class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    customer = serializers.SerializerMethodField()
    def get_customer(self, obj):
        customer = {
            'name': obj.customer.user.username
        }
        return customer

    # items = serializers.SerializerMethodField()
    # def get_items(self, obj):
    #     items = []
    #     for order_item in obj.items.all():
    #         item_data = {
    #             'product_name': order_item.name,
    #             # 'quantity': order_item
    #         }
    #         items.append(item_data)
    #     return items