# Generated by Django 5.0.1 on 2024-02-06 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='direktorat',
            field=models.CharField(blank=True, choices=[('psm', 'PSM'), ('dayatif', 'Dayatif')], default='dayatif', max_length=12, null=True),
        ),
    ]
