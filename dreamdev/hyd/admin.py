from django.contrib import admin
from .models import *

@admin.register(Ticket)
class ticketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id','issue_type','related_application_number', 'supporting_documents','description','name','phone_number','email')





@admin.register(DSATicket)
class DSATicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'issue_type', 'created_at', 'name','phone_number','email')
    list_filter = ('issue_type', )
    search_fields = ('description', 'name', 'phone_number','email')
    ordering = ('-created_at',)






class FranchiseeTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'issue_type', 'created_at', 'name', 'phone_number','email')
    list_filter = ('issue_type', 'created_at')
    search_fields = ('name', 'phone_number', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('issue_type', 'description', 'name', 'phone_number')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

admin.site.register(FranchiseeTicket, FranchiseeTicketAdmin)
admin.site.register(custmer)