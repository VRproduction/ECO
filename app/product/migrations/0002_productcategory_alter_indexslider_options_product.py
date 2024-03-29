# Generated by Django 5.0.1 on 2024-01-22 19:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='category')),
            ],
            options={
                'verbose_name': 'Kateqoriya',
                'verbose_name_plural': 'Kateqoriyalar',
            },
        ),
        migrations.AlterModelOptions(
            name='indexslider',
            options={'verbose_name': 'Slayder', 'verbose_name_plural': 'Ana səhifə | Slayder'},
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('badges', models.FloatField(blank=True, choices=[(1, 'Ən çox satılan'), (2, 'Yeni'), (3, 'Endirim'), (4, '4-cü')], null=True)),
                ('image', models.ImageField(upload_to='product')),
                ('price', models.FloatField()),
                ('discount', models.FloatField(null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.productcategory')),
            ],
            options={
                'verbose_name': 'Kateqoriya',
                'verbose_name_plural': 'Kateqoriyalar',
            },
        ),
    ]
