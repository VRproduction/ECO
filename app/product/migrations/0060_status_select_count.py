# Generated by Django 5.0.1 on 2024-03-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0059_alter_product_options_product_sale_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='select_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
