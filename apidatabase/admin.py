from django.contrib import admin

from apidatabase.models import *
'''
admin.site.register(Store)
admin.site.register(Customer)
admin.site.register(Queue)
admin.site.register(PromoCode)
admin.site.register(Advertisement)
admin.site.register(VaccinationCard)
'''
class StoreAdmin(admin.ModelAdmin):
    list_display = ['store_id','store_name', 'owner_first_name', 'owner_last_name', 'store_phone',
            'email', 'store_url', 'store_address','registration_date', 'store_capacity', 'password']
