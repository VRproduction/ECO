# Generated by Django 5.0.1 on 2024-02-02 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0041_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Gözləmədə', 'Pending'), ('İşlənir', 'Processing'), ('Göndərilib', 'Shipped'), ('Çatdırılıb', 'Delivered'), ('Ləğv edilib', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]