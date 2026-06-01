from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'unit_price', 'commission_percentage', 'created_at']
    search_fields = ['code', 'description']
    list_filter = ['commission_percentage']
    ordering = ['code']
