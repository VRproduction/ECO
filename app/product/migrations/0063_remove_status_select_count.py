# Generated by Django 5.0.1 on 2024-03-26 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0062_alter_status_select_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='status',
            name='select_count',
        ),
    ]
