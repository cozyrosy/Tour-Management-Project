from django.contrib import admin
from.models import ClientDetails

# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','address']
    search_fields=['first_name','last_name','phone','id__id']
admin.site.register(ClientDetails,CustomerAdmin)
