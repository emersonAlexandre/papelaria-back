"""Shared pytest fixtures."""
import pytest
from decimal import Decimal
from django.utils import timezone
from commissions.models import WeekdayCommissionRule
from people.models import Customer, Salesperson
from products.models import Product
from sales.models import Sale, SaleItem


@pytest.fixture
def weekday_rule():
    """A Monday commission rule: min 3%, max 5%."""
    return WeekdayCommissionRule(
        weekday=0,
        min_percentage=Decimal('3.00'),
        max_percentage=Decimal('5.00'),
    )


@pytest.fixture
def customer(db):
    return Customer.objects.create(
        name='João Silva',
        email='joao@exemplo.com',
        phone='81999990000',
    )


@pytest.fixture
def salesperson(db):
    return Salesperson.objects.create(
        name='Maria Vendas',
        email='maria@exemplo.com',
        phone='81988880000',
    )


@pytest.fixture
def product(db):
    return Product.objects.create(
        code='P001',
        description='Caderno universitário',
        unit_price=Decimal('25.00'),
        commission_percentage=Decimal('5.00'),
    )


@pytest.fixture
def sale(db, customer, salesperson, product):
    s = Sale.objects.create(
        invoice_number='00000001',
        sold_at=timezone.now(),
        customer=customer,
        salesperson=salesperson,
    )
    SaleItem.objects.create(sale=s, product=product, quantity=2)
    return s
