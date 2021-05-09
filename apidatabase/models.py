from django.db import models
from django.template.defaultfilters import slugify
import qrcode
import os
# Create your models here.
# Django will 
#   1) Creaet database tables(schemas) `Store` and `Queue`
#   2) Create a Python database-access API for accessing `Store` and `Queue` tables
#
# Refer to the page for support fields in Django
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types
class Store(models.Model):
    store_id  =  models.AutoField(primary_key=True)
    store_name = models.TextField(max_length=200)
    store_phone =  models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        """Make the representation of a Store object readable."""
        return "{id}:{name}:".format(id=self.store_id, name=self.store_name)

# Models used in queue feature-xm
class Store_q(models.Model):
    store_id  =  models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=128, unique=True)
    store_capacity = models.IntegerField(default=100)
    store_url = models.URLField()
    store_average_waiting_time_for_person = models.IntegerField(default=0)
    store_current_count = models.PositiveIntegerField(default = 0)
    slug = models.SlugField(unique=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.store_name)
        super(Store_q, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'stores'

    def __str__(self):
        return "{id}:{name}:".format(id=self.store_id, name=self.store_name)

class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True,blank=True, default = 0)
    store_id = models.PositiveIntegerField(blank=True, null=True)


    def __str__(self):
        """Make the representation of a Queue object readable."""
        return "{store_id}:{customer_id}".format(store_id=self.store_id, customer_id=self.customer_id)

# Models -xm
class Queue_q(models.Model):
    store = models.ForeignKey(Store_q, on_delete = models.CASCADE)
    queuedate = models.DateField()
    #current_customer_in_store = models.IntegerField(default=0)
    current_waiting_time = models.IntegerField(default=0)
    number_people_waiting = models.IntegerField(default=0)
    first_customer_queue_id = models.IntegerField(default=0)
    last_customer_queue_id = models.IntegerField(default=0)

    # def save(self,*args, **kwargs):
    #     if not self.pk:
    #         self.current_customer_in_store = self.store.capacity
    #     super(Queue_q,self).save(*args, **kwargs)
        
    def __str__(self):
        return str(self.queuedate)

class Customer_q(models.Model):
    store = models.ForeignKey(Store_q, on_delete = models.CASCADE)
    queue = models.ForeignKey(Queue_q, on_delete = models.CASCADE)
    customer_queue_id = models.IntegerField(default=0)
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