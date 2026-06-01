"""
Commission calculation service.

Applies weekday rules to clamp the product commission percentage,
then computes the total commission for each sale item.
"""
from decimal import Decimal
from typing import Optional

from .models import WeekdayCommissionRule


def _get_rule_for_date(sale_date) -> Optional[WeekdayCommissionRule]:
    """Return the WeekdayCommissionRule for the given date, or None."""
    weekday = sale_date.weekday()  # Monday=0, Sunday=6
    return WeekdayCommissionRule.objects.filter(weekday=weekday).first()


def apply_commission_rule(percentage: Decimal, rule: Optional[WeekdayCommissionRule]) -> Decimal:
    """
    Apply weekday rule clamping to a raw commission percentage.

    Args:
        percentage: Raw commission percentage from the product.
        rule: Optional WeekdayCommissionRule for the sale date.

    Returns:
        Effective commission percentage after applying the rule.
    """
    if rule is None:
        return percentage
    return max(rule.min_percentage, min(rule.max_percentage, percentage))


def calculate_item_commission(quantity: int, unit_price: Decimal, percentage: Decimal) -> Decimal:
    """
    Calculate commission for a single sale item.

    commission = quantity * unit_price * (percentage / 100)
    """
    return quantity * unit_price * (percentage / Decimal('100'))


def calculate_sale_commission(sale) -> Decimal:
    """
    Calculate total commission for a Sale instance.

    Fetches the weekday rule for the sale date and applies it to
    each item's product commission percentage.
    """
    rule = _get_rule_for_date(sale.sold_at.date())
    total = Decimal('0.00')

    for item in sale.items.select_related('product').all():
        effective_pct = apply_commission_rule(item.product.commission_percentage, rule)
        total += calculate_item_commission(item.quantity, item.product.unit_price, effective_pct)

    return total
