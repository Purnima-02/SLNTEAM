from django.contrib import admin

from AdminApp1.models import *


# Register your models here.

admin.site.register(SuperAdmin)
admin.site.register(SuperAdminApplications)
# admin.site.register(DSAMasterData)



@admin.register(DSAMasterData)
class DisbursmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DSAMasterData._meta.get_fields()]