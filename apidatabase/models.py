from django.db import models


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
    store_name = models.TextField(max_length=200)
    store_phone =  models.TextField(max_length=20)
    password = models.CharField(max_length=30, default=None)
    store_capacity = models.PositiveIntegerField(default = 0)
    store_current_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        """Make the representation of a Store object readable."""
        return "{id}:{name}:".format(id=self.store_id, name=self.store_name)


class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True,blank=True, default = 0)
    store_id = models.PositiveIntegerField(blank=True, null=True)


    def __str__(self):
        """Make the representation of a Queue object readable."""
        return "{store_id}:{customer_id}".format(store_id=self.store_id, customer_id=self.customer_id)