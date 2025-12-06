from django.contrib import admin
from .models.payout import Payout


@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency', 'created_at')
    search_fields = ('id', 'recipient_details', 'description')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('id', 'amount', 'currency', 'status')
        }),
        ('Реквизиты получателя', {
            'fields': ('recipient_details',)
        }),
        ('Дополнительно', {
            'fields': ('description', 'metadata')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )