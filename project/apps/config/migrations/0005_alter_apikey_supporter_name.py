# Generated by Django 4.2.11 on 2024-08-05 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_remove_apikey_customer_name_apikey_supporter_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='supporter_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Dəstəkçi (Məsələn: Logix, ...)'),
        ),
    ]