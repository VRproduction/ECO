# Generated by Django 5.0.1 on 2024-01-29 06:45

import ckeditor_uploader.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_blog'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='is_main_page',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='using_time',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='İstifadə müddəti'),
        ),
        migrations.AlterField(
            model_name='product',
            name='badges',
            field=models.IntegerField(blank=True, choices=[(1, 'Ən çox satılan'), (2, 'Yeni'), (3, 'Endirim'), (4, '4-cü')], null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='BasketItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', to='product.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='basket_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Səbət',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='product.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Sevimlilər',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sifariş',
                'verbose_name_plural': 'Sifarişlər',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='product.product')),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Məhsullar',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'verbose_name': 'Şəkil',
                'verbose_name_plural': 'Şəkillər',
            },
        ),
    ]
