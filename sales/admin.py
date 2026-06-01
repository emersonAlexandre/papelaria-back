from django.contrib import admin
from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'sold_at', 'customer', 'salesperson', 'total_value']
    list_filter = ['salesperson', 'customer', 'sold_at']
    search_fields = ['invoice_number', 'customer__name', 'salesperson__name']
    inlines = [SaleItemInline]
    ordering = ['-sold_at']
