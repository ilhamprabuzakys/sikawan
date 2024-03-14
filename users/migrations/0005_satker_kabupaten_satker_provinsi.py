# Generated by Django 5.0.1 on 2024-02-14 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
        ('users', '0004_profile_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='satker',
            name='kabupaten',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='kabupaten', to='masters.reg_regencies'),
        ),
        migrations.AddField(
            model_name='satker',
            name='provinsi',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='provinsi', to='masters.reg_provinces'),
        ),
    ]
