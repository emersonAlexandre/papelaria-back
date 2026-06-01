from rest_framework import serializers
from .models import Sale, SaleItem
from products.serializers import ProductSerializer


class SaleItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'subtotal']


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    salesperson_name = serializers.CharField(source='salesperson.name', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'sold_at',
            'customer', 'customer_name',
            'salesperson', 'salesperson_name',
            'items', 'total_value',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['invoice_number', 'created_at', 'updated_at']

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError(
                'A venda deve ter pelo menos um item.'
            )
        return items

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)
        for item in items_data:
            SaleItem.objects.create(sale=sale, **item)
        return sale

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                SaleItem.objects.create(sale=instance, **item)

        return instance


class SaleListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    salesperson_name = serializers.CharField(source='salesperson.name', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'invoice_number', 'sold_at',
            'customer', 'customer_name',
            'salesperson', 'salesperson_name',
            'total_value',
        ]
