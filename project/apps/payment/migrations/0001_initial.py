# Generated by Django 4.2.11 on 2024-08-01 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wolt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('customer_phone_number', models.CharField(blank=True, max_length=100, null=True)),
                ('customer_url', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50, unique=True)),
                ('payment_redirect_url', models.URLField(blank=True, null=True)),
                ('lat', models.CharField(blank=True, max_length=100, null=True)),
                ('lon', models.CharField(blank=True, max_length=100, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('recipient_name', models.CharField(blank=True, max_length=100, null=True)),
                ('recipient_phone', models.CharField(blank=True, max_length=100, null=True)),
                ('dropoff_comment', models.CharField(blank=True, max_length=100, null=True)),
                ('shipment_promise_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_wolt', models.BooleanField(default=False)),
                ('coupon_code', models.CharField(blank=True, max_length=100, null=True)),
                ('is_checked_from_eco', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
