from rest_framework.serializers import ModelSerializer
from .models import Transaction

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'value', 'payment_redirect_url', 'lat', 'lon', 'delivery_amount', 'recipient_name', 'recipient_phone', 'dropoff_comment', 'shipment_promise_id', 'is_wolt', 'coupon_code']  