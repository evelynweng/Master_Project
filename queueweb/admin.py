from django.contrib import admin

# Register your models here.
from apidatabase.models import Store, Queue, Customer

# add in this class to customise the admin interface
class storeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('store_name',)}

class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('join_time',)


admin.site.register(Store, storeAdmin)
admin.site.register(Queue)
admin.site.register(Customer, CustomerAdmin)
