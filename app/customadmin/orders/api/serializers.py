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
            'box_choice',
            'is_wolt',
            'transaction',
            'order_items'
        )


class OrderRetrieveUpdateDestroySerializer(serializers.ModelSerializer):
    order_items = OrderItemListSerializer(many=True, read_only=True)
    user = OrderUserListSerializer(read_only=True)
    transaction = TransactionListSerializer(read_only=True)
    is_wolt = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'order_type',
            'box_choice',
            'user',
            'is_wolt',
            'transaction',
            'order_items'
        )

    def get_is_wolt(self, obj):
        return obj.is_wolt

    # def validate(self, attrs):
    #     order_type = attrs.get('order_type')
    #     box_choice = attrs.get('box_choice')
    #     order_items = self.instance.order_items.all()
    #     for item in order_items:
    #         if item.product.stock <= 0:
    #             if order_type != 'Ləğv edilib':
    #                 raise serializers.ValidationError("Only you can change it to cancel if there are out-of-stock items.")
    #             if box_choice != None:
    #                 raise serializers.ValidationError("Only you can choose box if there are not out-of-stock items.")
    #     return super().validate(attrs)