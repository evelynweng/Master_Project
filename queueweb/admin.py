from django.contrib import admin

# Register your models here.
from apidatabase.models import *

# add in this class to customise the admin interface
class storeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('store_name',)}

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('join_time','id',)


admin.site.register(Store, storeAdmin)
admin.site.register(Queue)
admin.site.register(Advertisement)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(PromoCode)
admin.site.register(VaccinationCard)

