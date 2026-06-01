from decimal import Decimal
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import WeekdayCommissionRule
from .serializers import WeekdayCommissionRuleSerializer
from .services import calculate_sale_commission
from people.models import Salesperson
from sales.models import Sale


class WeekdayCommissionRuleViewSet(viewsets.ModelViewSet):
    """CRUD for weekday commission rules."""
    queryset = WeekdayCommissionRule.objects.all()
    serializer_class = WeekdayCommissionRuleSerializer
    ordering = ['weekday']


class CommissionReportView(APIView):
    """
    Returns a list of salespersons with their total commission
    for sales within the given date range.

    Query params:
        start_date (YYYY-MM-DD) — required
        end_date   (YYYY-MM-DD) — required
    """

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response(
                {'detail': 'Os parâmetros start_date e end_date são obrigatórios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from datetime import date
            start = date.fromisoformat(start_date)
            end = date.fromisoformat(end_date)
        except ValueError:
            return Response(
                {'detail': 'Formato de data inválido. Use YYYY-MM-DD.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start > end:
            return Response(
                {'detail': 'A data inicial não pode ser posterior à data final.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        sales = (
            Sale.objects
            .filter(sold_at__date__gte=start, sold_at__date__lte=end)
            .select_related('salesperson')
            .prefetch_related('items__product')
        )

        # Aggregate commissions per salesperson
        commission_map: dict[int, dict] = {}
        for sale in sales:
            sp = sale.salesperson
            if sp.id not in commission_map:
                commission_map[sp.id] = {
                    'id': sp.id,
                    'name': sp.name,
                    'email': sp.email,
                    'total_commission': Decimal('0.00'),
                    'total_sales': 0,
                }
            commission_map[sp.id]['total_commission'] += calculate_sale_commission(sale)
            commission_map[sp.id]['total_sales'] += 1

        results = sorted(commission_map.values(), key=lambda x: x['name'])
        total = sum(r['total_commission'] for r in results)

        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'salespersons': [
                {**r, 'total_commission': str(r['total_commission']), 'total_sales': r['total_sales']}
                for r in results
            ],
            'grand_total': str(total),
        })
