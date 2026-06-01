"""Integration tests for the Sales API."""
import pytest
from decimal import Decimal
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status

from sales.models import Sale, SaleItem


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestSaleAPI:
    def test_list_sales(self, api_client, sale):
        response = api_client.get('/api/sales/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_create_sale(self, api_client, customer, salesperson, product):
        payload = {
            'sold_at': timezone.now().isoformat(),
            'customer': customer.id,
            'salesperson': salesperson.id,
            'items': [{'product': product.id, 'quantity': 3}],
        }
        response = api_client.post('/api/sales/', payload, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Sale.objects.count() == 1

    def test_create_sale_without_items_fails(self, api_client, customer, salesperson):
        payload = {
            'sold_at': timezone.now().isoformat(),
            'customer': customer.id,
            'salesperson': salesperson.id,
            'items': [],
        }
        response = api_client.post('/api/sales/', payload, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_sale(self, api_client, sale):
        response = api_client.delete(f'/api/sales/{sale.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Sale.objects.count() == 0

    def test_total_value(self, api_client, sale, product):
        response = api_client.get(f'/api/sales/{sale.id}/')
        assert response.status_code == status.HTTP_200_OK
        # 2 items * R$25 = R$50
        assert Decimal(response.data['total_value']) == Decimal('50.00')
