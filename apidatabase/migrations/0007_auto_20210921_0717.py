# Generated by Django 3.0.7 on 2021-09-21 14:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apidatabase', '0006_auto_20210920_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='time_get_access',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
