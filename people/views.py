from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Customer, Salesperson
from .serializers import CustomerSerializer, SalespersonSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for customers."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class SalespersonViewSet(viewsets.ModelViewSet):
    """CRUD endpoint for salespersons."""
    queryset = Salesperson.objects.all()
    serializer_class = SalespersonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
