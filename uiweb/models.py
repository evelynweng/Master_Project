from django.db import models
from apidatabase.models import Store #import model Store from apidatabase
# Create your models here.
''' class Store(models.Model):
    store_id =  models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=30)
    owner_first_name = models.CharField(max_length=30)
    owner_last_name = models.CharField(max_length=30)
    store_phone = models.CharField(max_length=12) 
    email = models.EmailField(max_length=100)
    store_url =  models.URLField(max_length=200)
    store_address = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)
    #registration_date = models.DateField(default=date.today)
    store_capacity = models.IntegerField(null = True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.store_name '''