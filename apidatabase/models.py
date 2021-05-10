from django.db import models

from django.template.defaultfilters import slugify
import qrcode
import os

from django.utils import timezone


# Create your models here.
# Django will
#   1) Creaet database tables(schemas) `Store` and `Queue`
#   2) Create a Python database-access API for accessing `Store` and `Queue` tables
#
# Refer to the page for support fields in Django
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types

# store_id=1, store_name="KFC", store_phone =' 12345678', 
# password = 'testpwd', store_capacity=3

class Store(models.Model):
    store_id  =  models.AutoField(primary_key=True)

    store_name = models.TextField(max_length=50)
    store_phone =  models.TextField(max_length=12, unique= True,default='0')
    password = models.CharField(max_length=30)
    store_capacity = models.PositiveIntegerField(default = 0)
    store_current_count = models.PositiveIntegerField(default = 0)
    store_url = models.URLField(max_length = 200)
    store_average_waiting_time_for_person = models.IntegerField(default=0)
    store_current_count = models.PositiveIntegerField(default = 0)
    slug = models.SlugField(unique=True)
    owner_first_name = models.CharField(max_length=30)
    owner_last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    store_address = models.CharField(max_length=100)
    registration_date = models.DateTimeField(auto_now_add=True)	


    def save(self,*args, **kwargs):
        self.slug = slugify(self.store_name)
        super(Store, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'stores'


    def __str__(self):
        return "{id}:{name}:{phone}:{password}:{capacity}".format(
            id=self.store_id, 
            name=self.store_name, 
            phone=self.store_phone, 
            password = self.password, 
            capacity = self.store_capacity
            )


# Models -xm
class Queue(models.Model):
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    queuedate = models.DateField()
    #current_customer_in_store = models.IntegerField(default=0)
    current_waiting_time = models.IntegerField(default=0)
    number_people_waiting = models.IntegerField(default=0)
    first_Customerueue_id = models.IntegerField(default=0)
    last_Customerueue_id = models.IntegerField(default=0)

    # def save(self,*args, **kwargs):
    #     if not self.pk:
    #         self.current_customer_in_store = self.store.capacity
    #     super(Queue,self).save(*args, **kwargs)
        
    def __str__(self):
        return str(self.queuedate)

class Customer(models.Model):
    store = models.ForeignKey(Store, on_delete = models.CASCADE)
    queue = models.ForeignKey(Queue, on_delete = models.CASCADE)
    Customerueue_id = models.IntegerField(default=0)
    first_name = models.CharField(max_length=50, default = "XXX")
    last_name = models.CharField(max_length=50, default = "YYY")
    phone = models.CharField(max_length=50, default="XXX-XXX-XXXX")
    number_of_people = models.IntegerField(default=-1)
    join_time = models.TimeField(auto_now_add=True)
    #current_waiting_time_individual = models.IntegerField(default=-1)
    potential_wait_time = models.IntegerField(default=-1)
    #real_wait_time = models.IntegerField(default=-1)

    def __str__(self):
        return self.phone

