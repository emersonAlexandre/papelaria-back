from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import WeekdayCommissionRuleViewSet, CommissionReportView

router = DefaultRouter()
router.register('commission-rules', WeekdayCommissionRuleViewSet)

urlpatterns = router.urls + [
    path('commissions/report/', CommissionReportView.as_view(), name='commission-report'),
]
