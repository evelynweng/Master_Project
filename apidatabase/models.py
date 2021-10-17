from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator, MaxValueValidator,MinValueValidator
from PIL import Image
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

def ads_image_path(instance, filename):
    #return 'ads/ad_id_{0}/{1}'.format(instance.ad_id, filename)  
    return 'ads/store_id_{0}/ad_codes/{1}'.format(instance.store_id, filename)    

class Store(models.Model):

    '''  store_id = models.AutoField(primary_key=True)
     store_name = models.TextField(max_length=200)
     store_phone = models.PositiveIntegerField(blank=True, null=True)

     '''
    phone_message = 'Phone number must be entered in the format: xxx-xxx-xxxx' 
    phone_regex = RegexValidator(
        regex=r'^[\d]{3}-[\d]{3}-[\d]{4}',
        message=phone_message
    )

    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=30)
    owner_first_name = models.CharField(max_length=30,default='')
    owner_last_name = models.CharField(max_length=30,default='')
    store_phone = models.CharField(validators=[phone_regex],max_length=12,unique=True,default='')
    email = models.EmailField(max_length=100,default='',unique=True)
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
        return "{id}:{name}".format(id=self.store_id, name=self.store_name)

    """def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path) """   


class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True, blank=True, default=0)
    store_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        """Make the representation of a Queue object readable."""
        return "{store_id}:{customer_id}".format(store_id=self.store_id, customer_id=self.customer_id)

class Advertisement(models.Model):  
    store_id = models.ForeignKey(Store, on_delete = models.CASCADE, to_field='store_id')
    ad_id =  models.AutoField(primary_key=True)
    discount = models.IntegerField(default=0,
        validators=[MaxValueValidator(100), MinValueValidator(0)]) #in percentage
    ad_code = models.CharField(max_length=20)
    ad_image = models.ImageField(upload_to = ads_image_path)
    ad_description = models.CharField(max_length = 100,default="")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{store_id}:{ad_id}:{ad_code}".format(
            store_id=self.store_id,
            ad_id=self.ad_id, 
            ad_code=self.ad_code
            )

class PromoCode(models.Model):
    store_id = models.ForeignKey(Store, on_delete = models.CASCADE)
    promo_id =  models.AutoField(primary_key=True)
    discount = models.IntegerField(default=0) # added now
    promo_code = models.CharField(max_length=20)
    wait_time = models.IntegerField(default = 30)
    is_active = models.BooleanField(default=False)
    promo_description = models.CharField(max_length = 100,default="")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return str(self.promo_code)
