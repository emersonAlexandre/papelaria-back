"""Integration tests for the Products API."""
import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status

from products.models import Product


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestProductAPI:
    def test_list_products(self, api_client, product):
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_create_product(self, api_client):
        payload = {
            'code': 'TEST-001',
            'description': 'Produto teste',
            'unit_price': '12.50',
            'commission_percentage': '5.00',
        }
        response = api_client.post('/api/products/', payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Product.objects.filter(code='TEST-001').exists()

    def test_commission_percentage_max_10(self, api_client):
        payload = {
            'code': 'BAD-001',
            'description': 'Comissão inválida',
            'unit_price': '10.00',
            'commission_percentage': '15.00',  # > 10% — invalid
        }
        response = api_client.post('/api/products/', payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_commission_percentage_min_0(self, api_client):
        payload = {
            'code': 'BAD-002',
            'description': 'Comissão negativa',
            'unit_price': '10.00',
            'commission_percentage': '-1.00',  # negative — invalid
        }
        response = api_client.post('/api/products/', payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_search_product(self, api_client, product):
        response = api_client.get('/api/products/', {'search': product.code})
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_update_product(self, api_client, product):
        response = api_client.patch(
            f'/api/products/{product.id}/',
            {'unit_price': '30.00'}
        )
        assert response.status_code == status.HTTP_200_OK
        product.refresh_from_db()
        assert product.unit_price == Decimal('30.00')
