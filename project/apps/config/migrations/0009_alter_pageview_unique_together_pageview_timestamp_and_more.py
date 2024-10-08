# Generated by Django 4.2.11 on 2024-08-29 14:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_pageview'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='pageview',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='pageview',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddIndex(
            model_name='pageview',
            index=models.Index(fields=['url', 'ip_address', 'timestamp'], name='config_page_url_002983_idx'),
        ),
        migrations.RemoveField(
            model_name='pageview',
            name='date',
        ),
    ]
