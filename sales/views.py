import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Sale
from .serializers import SaleSerializer, SaleListSerializer


class SaleFilter(django_filters.FilterSet):
    sold_at_after = django_filters.DateFilter(field_name='sold_at', lookup_expr='date__gte')
    sold_at_before = django_filters.DateFilter(field_name='sold_at', lookup_expr='date__lte')
    customer = django_filters.NumberFilter(field_name='customer__id')
    salesperson = django_filters.NumberFilter(field_name='salesperson__id')

    class Meta:
        model = Sale
        fields = ['customer', 'salesperson', 'sold_at_after', 'sold_at_before']


class SaleViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for sales."""
    queryset = (
        Sale.objects
        .select_related('customer', 'salesperson')
        .prefetch_related('items__product')
    )
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = SaleFilter
    search_fields = ['invoice_number', 'customer__name', 'salesperson__name']
    ordering_fields = ['sold_at', 'invoice_number']
    ordering = ['-sold_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return SaleListSerializer
        return SaleSerializer
