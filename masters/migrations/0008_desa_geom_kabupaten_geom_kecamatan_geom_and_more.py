# Generated by Django 5.0.1 on 2024-02-21 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0007_alter_kawasanrawan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='desa',
            name='geom',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='kabupaten',
            name='geom',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='kecamatan',
            name='geom',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='provinsi',
            name='geom',
            field=models.JSONField(null=True),
        ),
    ]
