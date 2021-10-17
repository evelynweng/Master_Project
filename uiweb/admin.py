from django.db import models
from apidatabase.models import Advertisement, PromoCode
from django.contrib import admin

# Register your models here.
from .models import Store
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id','store_name', 'owner_first_name', 'owner_last_name', 'store_phone',
            'email', 'store_url', 'store_address','registration_date', 'store_capacity', 'password']
admin.site.register(Store,StoreAdmin)


class AdvertisementAdmin(admin.ModelAdmin):
    list_display=['store_id', 'ad_id','discount','ad_image','ad_description','start_date','end_date']

admin.site.register(Advertisement,AdvertisementAdmin)

class PromoCodeAdmin(admin.ModelAdmin):
    list_display=['store_id', 'promo_id','discount','promo_code','wait_time','is_active','promo_description','start_date','end_date']

admin.site.register(PromoCode,PromoCodeAdmin)


