# Generated by Django 5.0.1 on 2024-02-11 08:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='reg_provinces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_provinsi', models.CharField(max_length=10)),
                ('nama_provinsi', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
            ],
            options={
                'verbose_name': 'Provinsi',
                'verbose_name_plural': 'Daftar Provinsi',
                'ordering': ['-latitude'],
            },
        ),
        migrations.CreateModel(
            name='reg_regencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_kabupaten', models.CharField(max_length=10)),
                ('nama_kabupaten', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('kode_provinsi', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.reg_provinces')),
            ],
            options={
                'verbose_name': 'Kabupaten',
                'verbose_name_plural': 'Daftar Kabupaten',
            },
        ),
        migrations.CreateModel(
            name='reg_district',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_kecamatan', models.CharField(max_length=10)),
                ('nama_kecamatan', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('kode_kabupaten', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.reg_regencies')),
            ],
            options={
                'verbose_name': 'Kecamatan',
                'verbose_name_plural': 'Daftar Kecamatan',
            },
        ),
        migrations.CreateModel(
            name='reg_villages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kode_desa', models.CharField(max_length=10)),
                ('nama_desa', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),
                ('kode_kecamatan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.reg_district')),
            ],
            options={
                'verbose_name': 'Desa',
                'verbose_name_plural': 'Daftar Desa',
            },
        ),
        migrations.CreateModel(
            name='KawasanRawan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('bahaya', 'Bahaya'), ('waspada', 'Waspada'), ('siaga', 'Siaga'), ('aman', 'Aman')], max_length=15, null=True)),
                ('tahun', models.CharField(blank=True, choices=[('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024')], max_length=4, null=True)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kawan_created_by', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kawan_updated_by', to=settings.AUTH_USER_MODEL)),
                ('desa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kawasan_rawan', to='masters.reg_villages')),
            ],
            options={
                'verbose_name': 'Kawasan Rawan',
                'verbose_name_plural': 'Daftar Kawasan Rawan',
                'db_table': 'masters_kawasan_rawan',
            },
        ),
    ]
