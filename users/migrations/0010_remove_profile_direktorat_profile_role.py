# Generated by Django 5.0.1 on 2024-03-09 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_satkerbnnk_satkerbnnp_remove_profile_is_verified_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='direktorat',
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(blank=True, choices=[('superadmin', 'Super Admin'), ('bnnp', 'BNNP'), ('bnnk', 'BNNK')], default='bnnk', max_length=20, null=True),
        ),
    ]