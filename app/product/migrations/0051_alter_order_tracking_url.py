# Generated by Django 5.0.1 on 2024-03-17 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0050_alter_order_tracking_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
