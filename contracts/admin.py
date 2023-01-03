from django.contrib import admin
from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contract Info', {'fields': ('client', 'amount', 'payment_due')}),
        ('Sales', {'fields': ('is_signed', 'sales_contact')}),#contract_status
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('contract_number', 'sales_contact', 'client_id', 'amount', 'payment_due', 'is_signed')
    list_filter = ('is_signed', 'sales_contact', 'date_created',)
    search_fields = ('contract_number', 'client__last_name')

    @staticmethod
    def contract_number(obj):
        return f"Contract Nº{obj.id}"
        