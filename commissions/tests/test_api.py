"""Integration tests for the Commission Report API."""
import pytest
from decimal import Decimal
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestCommissionReportAPI:
    def test_report_requires_dates(self, api_client):
        response = api_client.get('/api/commissions/report/')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_report_returns_salesperson_commissions(self, api_client, sale):
        today = timezone.now().date().isoformat()
        response = api_client.get(
            '/api/commissions/report/',
            {'start_date': today, 'end_date': today}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['salespersons']) == 1
        sp = response.data['salespersons'][0]
        # 2 * R$25 * 5% = R$2.50
        assert Decimal(sp['total_commission']) == Decimal('2.50')
        assert Decimal(response.data['grand_total']) == Decimal('2.50')

    def test_report_empty_when_no_sales_in_period(self, api_client, sale):
        response = api_client.get(
            '/api/commissions/report/',
            {'start_date': '2000-01-01', 'end_date': '2000-01-31'}
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['salespersons'] == []
        assert Decimal(response.data['grand_total']) == Decimal('0')

    def test_report_invalid_date_format(self, api_client):
        response = api_client.get(
            '/api/commissions/report/',
            {'start_date': '01/01/2024', 'end_date': '31/01/2024'}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
