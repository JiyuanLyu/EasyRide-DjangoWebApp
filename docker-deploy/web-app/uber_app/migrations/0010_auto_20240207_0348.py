# Generated by Django 2.2.28 on 2024-02-07 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uber_app', '0009_user_is_active_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridesharer',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
