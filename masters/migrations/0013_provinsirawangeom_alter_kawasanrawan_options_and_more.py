# Generated by Django 5.0.1 on 2024-02-26 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0012_provinsirawan'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProvinsiRawanGeom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', models.CharField(max_length=300)),
                ('tahun', models.CharField(max_length=4)),
            ],
            options={
                'db_table': 'masters_provinsi_rawan_geom',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='kawasanrawan',
            options={'ordering': ['updated_at'], 'verbose_name': 'Kawasan Rawan', 'verbose_name_plural': 'Daftar Kawasan Rawan'},
        ),
        migrations.AddField(
            model_name='provinsi',
            name='latitude2',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='provinsi',
            name='longitude2',
            field=models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True),
        ),
    ]
