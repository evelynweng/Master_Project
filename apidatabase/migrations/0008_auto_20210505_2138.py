# Generated by Django 3.0.7 on 2021-05-06 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apidatabase', '0007_customer_q_customer_queue_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue_q',
            name='first_customer_queue_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='queue_q',
            name='last_customer_queue_id',
            field=models.IntegerField(default=0),
        ),
    ]