# Generated by Django 4.2.11 on 2024-08-05 16:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('config', '0006_alter_apikey_supporter_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikey',
            name='supporter_name',
        ),
        migrations.AddField(
            model_name='apikey',
            name='supporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='api_keys', to='core.supporter', verbose_name='Dəstəkçi (Məsələn: Logix, ...)'),
        ),
    ]
