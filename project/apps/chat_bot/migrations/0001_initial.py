# Generated by Django 4.2.11 on 2024-08-05 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supporter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Dəstəkçi (Məsələn: Logix, ...)')),
            ],
        ),
    ]
