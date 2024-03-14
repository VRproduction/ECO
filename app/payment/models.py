from django.db import models

class Wolt(models.Model):
    customer_email = models.EmailField(blank = True, null = True)
    customer_phone_number = models.CharField(max_length = 100, blank = True, null = True)
    customer_url = models.TextField(null = True, blank = True)

    def __str__(self) -> str:
        return 'WOLT'