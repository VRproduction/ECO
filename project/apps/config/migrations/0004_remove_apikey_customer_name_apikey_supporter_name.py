# Generated by Django 4.2.11 on 2024-08-05 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_apikey_is_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='apikey',
            name='supporter_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Dəstəkçi (Logix)'),
        ),
    ]
