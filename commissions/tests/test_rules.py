"""Tests for the WeekdayCommissionRule model and API."""
import pytest
from decimal import Decimal
from rest_framework.test import APIClient
from rest_framework import status

from commissions.models import WeekdayCommissionRule


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestWeekdayCommissionRuleAPI:
    def test_create_rule(self, api_client):
        payload = {'weekday': 0, 'min_percentage': '3.00', 'max_percentage': '5.00'}
        response = api_client.post('/api/commission-rules/', payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert WeekdayCommissionRule.objects.count() == 1

    def test_min_greater_than_max_fails(self, api_client):
        payload = {'weekday': 1, 'min_percentage': '8.00', 'max_percentage': '3.00'}
        response = api_client.post('/api/commission-rules/', payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_weekday_fails(self, api_client):
        api_client.post('/api/commission-rules/', {'weekday': 2, 'min_percentage': '1', 'max_percentage': '5'})
        response = api_client.post('/api/commission-rules/', {'weekday': 2, 'min_percentage': '2', 'max_percentage': '6'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_rules(self, api_client):
        WeekdayCommissionRule.objects.create(weekday=0, min_percentage=Decimal('3'), max_percentage=Decimal('5'))
        response = api_client.get('/api/commission-rules/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_weekday_display_in_response(self, api_client):
        WeekdayCommissionRule.objects.create(weekday=0, min_percentage=Decimal('2'), max_percentage=Decimal('4'))
        response = api_client.get('/api/commission-rules/')
        assert response.data['results'][0]['weekday_display'] == 'Segunda-Feira'
