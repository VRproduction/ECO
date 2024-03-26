from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wolt(models.Model):
    customer_email = models.EmailField(blank = True, null = True)
    customer_phone_number = models.CharField(max_length = 100, blank = True, null = True)
    customer_url = models.TextField(null = True, blank = True)

    def __str__(self) -> str:
        return 'WOLT'
    
class Transaction(models.Model):
    value = models.CharField(max_length = 50, unique = True)
    payment_redirect_url = models.URLField(null = True, blank = True)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, null = True)
    lat = models.CharField(max_length = 100, null = True, blank = True)
    lon = models.CharField(max_length = 100, null = True, blank = True)
    amount = models.CharField(max_length = 100, null = True, blank = True)
    recipient_name = models.CharField(max_length = 100, null = True, blank = True)
    recipient_phone = models.CharField(max_length = 100, null = True, blank = True)
    dropoff_comment = models.CharField(max_length = 100, null = True, blank = True)
    shipment_promise_id = models.CharField(max_length = 100, null = True, blank = True)
    is_wolt = models.BooleanField(default = False)
    coupon_code= models.CharField(max_length = 100, null = True, blank = True)
    is_checked_from_eco = models.BooleanField(default = False)
    
    def __str__(self) -> str:
        return self.value