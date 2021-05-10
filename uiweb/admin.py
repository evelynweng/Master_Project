from django.contrib import admin

# Register your models here.
from .models import Store
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id','store_name', 'owner_first_name', 'owner_last_name', 'store_phone',
            'email', 'store_url', 'store_address','registration_date', 'store_capacity', 'password']
#admin.site.register(Store,StoreAdmin)
