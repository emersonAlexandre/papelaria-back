from rest_framework import serializers
from .models import Customer, Salesperson


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class SalespersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salesperson
        fields = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
