# Generated by Django 5.0.1 on 2024-03-18 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_transaction_is_checked_from_eco'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='delivery_redirect_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]