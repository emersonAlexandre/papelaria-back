"""Unit tests for the commission calculation service."""
from decimal import Decimal
import pytest
from commissions.services import apply_commission_rule, calculate_item_commission


class TestApplyCommissionRule:
    def test_no_rule_returns_original(self):
        assert apply_commission_rule(Decimal('5.00'), None) == Decimal('5.00')

    def test_clamps_above_max(self, weekday_rule):
        # Product commission 10%, rule max 5% → should be clamped to 5%
        result = apply_commission_rule(Decimal('10.00'), weekday_rule)
        assert result == Decimal('5.00')

    def test_clamps_below_min(self, weekday_rule):
        # Product commission 1%, rule min 3% → should be clamped to 3%
        result = apply_commission_rule(Decimal('1.00'), weekday_rule)
        assert result == Decimal('3.00')

    def test_within_range_unchanged(self, weekday_rule):
        # Product commission 4%, rule 3–5% → stays 4%
        result = apply_commission_rule(Decimal('4.00'), weekday_rule)
        assert result == Decimal('4.00')


class TestCalculateItemCommission:
    def test_basic_calculation(self):
        # 2 units * R$100 * 5% = R$10
        result = calculate_item_commission(2, Decimal('100.00'), Decimal('5.00'))
        assert result == Decimal('10.00')

    def test_zero_percentage(self):
        result = calculate_item_commission(5, Decimal('200.00'), Decimal('0.00'))
        assert result == Decimal('0.00')

    def test_fractional_result(self):
        result = calculate_item_commission(3, Decimal('10.00'), Decimal('7.50'))
        assert result == Decimal('2.25')
