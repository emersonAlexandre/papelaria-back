"""
Management command: seed_demo
Populates the database with sample data for development.

Usage:
    python manage.py seed_demo
"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from people.models import Customer, Salesperson
from products.models import Product
from sales.models import Sale, SaleItem
from commissions.models import WeekdayCommissionRule


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱  Seeding demo data…')

        # Weekday rules
        WeekdayCommissionRule.objects.get_or_create(
            weekday=0,
            defaults={'min_percentage': Decimal('3'), 'max_percentage': Decimal('5')}
        )
        WeekdayCommissionRule.objects.get_or_create(
            weekday=4,
            defaults={'min_percentage': Decimal('1'), 'max_percentage': Decimal('8')}
        )

        # Salespersons
        sp1, _ = Salesperson.objects.get_or_create(
            email='ana@papelaria.com',
            defaults={'name': 'Ana Souza', 'phone': '81999990001'}
        )
        sp2, _ = Salesperson.objects.get_or_create(
            email='carlos@papelaria.com',
            defaults={'name': 'Carlos Lima', 'phone': '81999990002'}
        )

        # Customers
        c1, _ = Customer.objects.get_or_create(
            email='escola@exemplo.com',
            defaults={'name': 'Escola Municipal ABC', 'phone': '8133330001'}
        )
        c2, _ = Customer.objects.get_or_create(
            email='escritorio@exemplo.com',
            defaults={'name': 'Escritório Central', 'phone': '8133330002'}
        )

        # Products
        p1, _ = Product.objects.get_or_create(
            code='CAD-001',
            defaults={'description': 'Caderno 96 folhas', 'unit_price': Decimal('15.90'), 'commission_percentage': Decimal('5')}
        )
        p2, _ = Product.objects.get_or_create(
            code='CAN-010',
            defaults={'description': 'Caneta esferográfica azul', 'unit_price': Decimal('2.50'), 'commission_percentage': Decimal('3')}
        )
        p3, _ = Product.objects.get_or_create(
            code='LAP-005',
            defaults={'description': 'Lápis HB caixa c/12', 'unit_price': Decimal('8.00'), 'commission_percentage': Decimal('7')}
        )

        # Sales
        s = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=2),
            customer=c1,
            salesperson=sp1,
        )
        SaleItem.objects.create(sale=s, product=p1, quantity=10)
        SaleItem.objects.create(sale=s, product=p2, quantity=50)

        s2 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s2, product=p3, quantity=5)
        SaleItem.objects.create(sale=s2, product=p1, quantity=3)

        s3 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s3, product=p3, quantity=5)
        SaleItem.objects.create(sale=s3, product=p1, quantity=3)

        s4 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s4, product=p3, quantity=5)
        SaleItem.objects.create(sale=s4, product=p1, quantity=3)

        s5 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s5, product=p3, quantity=5)
        SaleItem.objects.create(sale=s5, product=p1, quantity=3)

        s6 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s6, product=p3, quantity=5)
        SaleItem.objects.create(sale=s6, product=p1, quantity=3)

        s7 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s7, product=p3, quantity=5)
        SaleItem.objects.create(sale=s7, product=p1, quantity=3)

        s8 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s8, product=p3, quantity=5)
        SaleItem.objects.create(sale=s8, product=p1, quantity=3)

        s9 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s9, product=p3, quantity=5)
        SaleItem.objects.create(sale=s9, product=p1, quantity=3)

        s10 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s10, product=p3, quantity=5)
        SaleItem.objects.create(sale=s10, product=p1, quantity=3)

        s11 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s11, product=p3, quantity=5)
        SaleItem.objects.create(sale=s11, product=p1, quantity=3)

        s12 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s12, product=p3, quantity=5)
        SaleItem.objects.create(sale=s12, product=p1, quantity=3)

        s13 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s13, product=p3, quantity=5)
        SaleItem.objects.create(sale=s13, product=p1, quantity=3)

        s14 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s14, product=p3, quantity=5)
        SaleItem.objects.create(sale=s14, product=p1, quantity=3)

        s15 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s15, product=p3, quantity=5)
        SaleItem.objects.create(sale=s15, product=p1, quantity=3)

        s16 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s16, product=p3, quantity=5)
        SaleItem.objects.create(sale=s16, product=p1, quantity=3)

        s17 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s17, product=p3, quantity=5)
        SaleItem.objects.create(sale=s17, product=p1, quantity=3)

        s18 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s18, product=p3, quantity=5)
        SaleItem.objects.create(sale=s18, product=p1, quantity=3)

        s19 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s19, product=p3, quantity=5)
        SaleItem.objects.create(sale=s19, product=p1, quantity=3)

        s20 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s20, product=p3, quantity=5)
        SaleItem.objects.create(sale=s20, product=p1, quantity=3)

        s21 = Sale.objects.create(
            sold_at=timezone.now() - timedelta(days=1),
            customer=c2,
            salesperson=sp2,
        )
        SaleItem.objects.create(sale=s21, product=p3, quantity=5)
        SaleItem.objects.create(sale=s21, product=p1, quantity=3)

        self.stdout.write(self.style.SUCCESS('✅  Demo data seeded successfully.'))
