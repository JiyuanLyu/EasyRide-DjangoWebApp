# Generated by Django 4.2.9 on 2024-02-01 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('uber_app', '0004_alter_ride_ownerid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='driverID',
            new_name='driver',
        ),
        migrations.RenameField(
            model_name='ridesharer',
            old_name='rideID',
            new_name='share_ride',
        ),
        migrations.RenameField(
            model_name='ridesharer',
            old_name='userID',
            new_name='share_user',
        ),
    ]