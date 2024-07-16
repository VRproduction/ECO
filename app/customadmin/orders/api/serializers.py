from django.contrib.auth import get_user_model

from rest_framework import serializers

from product.models import (
    Order,
    OrderItem,
    Product,
    Transaction
)

User = get_user_model()

class OrderUserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            'id',
            'full_name',
            'email'
        )
    
    def get_full_name(self, obj):
        return obj.get_full_name()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class TransactionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'recipient_name',
            'recipient_phone',
            'dropoff_comment'
        )


class OrderItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'quantity'
        )


class OrderListSerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True)
    user = OrderUserListSerializer()
    transaction = TransactionListSerializer()

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'order_type',
            'is_wolt',
            'transaction',
            'order_items'
        )


class OrderUpdateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'order_type'
        )