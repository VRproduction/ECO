# Generated by Django 4.2.11 on 2024-08-02 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_title', models.CharField(max_length=200, verbose_name='Saytın başlığı')),
                ('site_title_az', models.CharField(max_length=200, null=True, verbose_name='Saytın başlığı')),
                ('site_title_en', models.CharField(max_length=200, null=True, verbose_name='Saytın başlığı')),
                ('site_title_ru', models.CharField(max_length=200, null=True, verbose_name='Saytın başlığı')),
                ('adress', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Ünvan')),
                ('adress_az', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Ünvan')),
                ('adress_en', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Ünvan')),
                ('adress_ru', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Ünvan')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('g_adress', models.CharField(blank=True, max_length=1500, null=True, verbose_name='Google Map linki')),
                ('g_adress_iframe', models.TextField(blank=True, null=True, verbose_name='Google Map Iframe linki')),
                ('logo', models.FileField(blank=True, upload_to='general_settings_logo', verbose_name='logo(171x38)')),
                ('mobile_logo', models.FileField(blank=True, help_text='Mobile logo', null=True, upload_to='general_settings_mobile_logo', verbose_name='Mobile logo(172x38)')),
                ('favicon', models.FileField(blank=True, null=True, upload_to='general_settings_favicon', verbose_name='favicon(100x100)')),
                ('footer_logo', models.FileField(blank=True, help_text='Footer logo', null=True, upload_to='general_settings_footer_logo')),
                ('footer_slogan', models.TextField(blank=True, null=True)),
                ('footer_slogan_az', models.TextField(blank=True, null=True)),
                ('footer_slogan_en', models.TextField(blank=True, null=True)),
                ('footer_slogan_ru', models.TextField(blank=True, null=True)),
                ('copyright_title', models.CharField(blank=True, max_length=100)),
                ('copyright_title_az', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright_title_en', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright_title_ru', models.CharField(blank=True, max_length=100, null=True)),
                ('copyright_link', models.TextField(blank=True, null=True)),
                ('facebook', models.CharField(blank=True, max_length=200, verbose_name='Facebook')),
                ('instagram', models.CharField(blank=True, max_length=200, verbose_name='Instagram')),
                ('youtube', models.CharField(blank=True, max_length=200, verbose_name='Youtube')),
                ('tiktok', models.CharField(blank=True, max_length=200, verbose_name='TikTok')),
                ('work_start_hour', models.TimeField(null=True, verbose_name='İşin başlama saatı')),
                ('work_finish_hour', models.TimeField(null=True, verbose_name='İşin bitmə saatı')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'General Settings',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=200, null=True)),
                ('is_main', models.BooleanField(default=False)),
                ('setting', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='numbers', to='config.generalsettings')),
            ],
            options={
                'verbose_name': 'Nömrə',
                'verbose_name_plural': 'Nömrələr',
            },
        ),
    ]
