from django.db import models
from django.utils import timezone

# Create your models here.
# Django will
#   1) Creaet database tables(schemas) `Store` and `Queue`
#   2) Create a Python database-access API for accessing `Store` and `Queue` tables
#
# Refer to the page for support fields in Django
# https://docs.djangoproject.com/en/3.1/ref/models/fields/#field-types

def profile_pic_path(instance, filename):  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'profile_pics/store_id_{0}/{1}'.format(instance.store_id, filename)

class Store(models.Model):

    '''  store_id = models.AutoField(primary_key=True)
     store_name = models.TextField(max_length=200)
     store_phone = models.PositiveIntegerField(blank=True, null=True)

     '''
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=30)
    owner_first_name = models.CharField(max_length=30,default='')
    owner_last_name = models.CharField(max_length=30,default='')
    store_phone = models.CharField(max_length=12,unique=True,default='')
    email = models.EmailField(max_length=100,default='')
    store_url = models.URLField(max_length=200,default='')
    store_address = models.CharField(max_length=100,default='')
    registration_date = models.DateTimeField(auto_now_add=True)
    # registration_date = models.DateField(default=date.today)
    store_capacity = models.IntegerField(default=0)
    password = models.CharField(max_length=30, null=False,default='')
    is_email_verified = models.BooleanField(default=False)
    profile_pic = models.ImageField(default = 'default.jpg' , upload_to = profile_pic_path)

    def __str__(self):
        """Make the representation of a Store object readable."""
        return "{id}:{name}:".format(id=self.store_id, name=self.store_name)


class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True, blank=True, default=0)
    store_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        """Make the representation of a Queue object readable."""
        return "{store_id}:{customer_id}".format(store_id=self.store_id, customer_id=self.customer_id)
