from django.contrib import admin
from .models import WeekdayCommissionRule


@admin.register(WeekdayCommissionRule)
class WeekdayCommissionRuleAdmin(admin.ModelAdmin):
    list_display = ['get_weekday_display', 'min_percentage', 'max_percentage']
    ordering = ['weekday']
