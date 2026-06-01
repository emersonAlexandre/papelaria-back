"""Integration tests for the People API (Customers & Salespersons)."""
import pytest
from rest_framework.test import APIClient
from rest_framework import status

from people.models import Customer, Salesperson


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestCustomerAPI:
    def test_list_customers(self, api_client, customer):
        response = api_client.get('/api/customers/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_create_customer(self, api_client):
        payload = {'name': 'Novo Cliente', 'email': 'novo@exemplo.com', 'phone': '81900000000'}
        response = api_client.post('/api/customers/', payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(email='novo@exemplo.com').exists()

    def test_create_customer_duplicate_email_fails(self, api_client, customer):
        payload = {'name': 'Outro', 'email': customer.email, 'phone': '81911111111'}
        response = api_client.post('/api/customers/', payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_customer(self, api_client, customer):
        response = api_client.patch(f'/api/customers/{customer.id}/', {'name': 'Nome Novo'})
        assert response.status_code == status.HTTP_200_OK
        customer.refresh_from_db()
        assert customer.name == 'Nome Novo'

    def test_delete_customer(self, api_client, customer):
        response = api_client.delete(f'/api/customers/{customer.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestSalespersonAPI:
    def test_list_salespersons(self, api_client, salesperson):
        response = api_client.get('/api/salespersons/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_create_salesperson(self, api_client):
        payload = {'name': 'Novo Vendedor', 'email': 'vendedor@exemplo.com', 'phone': '81922222222'}
        response = api_client.post('/api/salespersons/', payload)
        assert response.status_code == status.HTTP_201_CREATED
