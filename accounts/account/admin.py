from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(DisbursementData)
admin.site.register(InputWindow)
admin.site.register(Disbursement)
admin.site.register(DisbursementDetail)
admin.site.register(SettlementWindow)