# Generated by Django 4.2.11 on 2024-11-26 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_alter_productcategory_title_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]