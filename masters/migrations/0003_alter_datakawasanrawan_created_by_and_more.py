# Generated by Django 5.0.1 on 2024-02-15 03:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0002_desa_kabupaten_provinsi_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='datakawasanrawan',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_kawan_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='datakawasanrawan',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_kawan_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='kawasanrawan',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kawan_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='kawasanrawan',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kawan_updated_by', to=settings.AUTH_USER_MODEL),
        ),
    ]