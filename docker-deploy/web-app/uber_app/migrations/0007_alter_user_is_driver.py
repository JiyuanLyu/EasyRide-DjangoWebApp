# Generated by Django 4.2.9 on 2024-02-04 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uber_app', '0006_alter_user_is_driver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_driver',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
