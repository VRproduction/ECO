# Generated by Django 4.2.11 on 2024-07-20 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0093_remove_orderitem_box_choice_order_box_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='box_choice',
            field=models.CharField(blank=True, choices=[('Kiçik', 'Kiçik'), ('Orta', 'Orta'), ('Böyük', 'Böyük')], max_length=20, null=True, verbose_name='Qutu seçimi'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]