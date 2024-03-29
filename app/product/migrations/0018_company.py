# Generated by Django 5.0.1 on 2024-01-26 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_alter_feature_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount', models.FloatField(blank=True, null=True)),
                ('finish_time', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('product', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company', to='product.product')),
            ],
            options={
                'verbose_name': 'Kompaniya',
                'verbose_name_plural': 'Kompaniyalar',
            },
        ),
    ]
