# Generated by Django 3.2 on 2021-10-27 18:32

import apidatabase.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apidatabase', '0009_merge_20211016_2251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='store_average_waiting_time_for_person',
        ),
        migrations.RemoveField(
            model_name='store',
            name='store_current_count',
        ),
        migrations.AddField(
            model_name='advertisement',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='store',
            name='is_email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='store',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to=apidatabase.models.profile_pic_path),
        ),
        migrations.AlterField(
            model_name='advertisement',
            name='store_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='apidatabase.store'),
        ),
        migrations.AlterField(
            model_name='store',
            name='email',
            field=models.EmailField(default='', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='store',
            name='owner_first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='store',
            name='owner_last_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='store',
            name='password',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_capacity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_phone',
            field=models.CharField(default='', max_length=12, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must be entered in the format: xxx-xxx-xxxx', regex='^[\\d]{3}-[\\d]{3}-[\\d]{4}')]),
        ),
        migrations.AlterField(
            model_name='store',
            name='store_url',
            field=models.URLField(default=''),
        ),
    ]
