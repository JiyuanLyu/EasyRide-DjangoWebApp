# Generated by Django 4.2.9 on 2024-02-01 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uber_app', '0005_rename_driverid_ride_driver_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
