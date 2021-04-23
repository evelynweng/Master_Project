# Generated by Django 2.2.12 on 2021-04-23 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.PositiveIntegerField()),
                ('customer_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.PositiveIntegerField()),
                ('store_name', models.TextField(max_length=200)),
            ],
        ),
    ]
