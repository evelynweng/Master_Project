from django.contrib import admin

# Register your models here.
from apidatabase.models import Store_q, Queue_q, Customer_q

# add in this class to customise the admin interface
class storeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class Customer_qAdmin(admin.ModelAdmin):
    readonly_fields = ('join_time',)


admin.site.register(Store_q, storeAdmin)
admin.site.register(Queue_q)
admin.site.register(Customer_q, Customer_qAdmin)
