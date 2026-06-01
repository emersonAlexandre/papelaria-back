from django.db import models
from people.models import Customer, Salesperson
from products.models import Product


class Sale(models.Model):
    """Sale (nota fiscal) with items."""
    invoice_number = models.CharField('Número da Nota Fiscal', max_length=50, unique=True, blank=True, editable=False)
    sold_at = models.DateTimeField('Data/Hora da Venda')
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT,
        verbose_name='Cliente', related_name='sales'
    )
    salesperson = models.ForeignKey(
        Salesperson, on_delete=models.PROTECT,
        verbose_name='Vendedor', related_name='sales'
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-sold_at']

    def __str__(self):
        return f'NF {self.invoice_number} — {self.sold_at:%d/%m/%Y %H:%M}'

    @property
    def total_value(self):
        from django.db.models import Sum, F, DecimalField, ExpressionWrapper
        result = self.items.aggregate(
            total=Sum(
                ExpressionWrapper(
                    F('quantity') * F('product__unit_price'),
                    output_field=DecimalField()
                )
            )
        )
        return result['total'] or 0

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = self._generate_invoice_number()
        super().save(*args, **kwargs)

    @staticmethod
    def _generate_invoice_number():
        last = Sale.objects.order_by('invoice_number').last()

        if last:
            sequence = int(last.invoice_number) + 1
        else:
            sequence = 1

        return f'{sequence:08d}'
        # gera: 00000001, 00000002, etc.


class SaleItem(models.Model):
    """Individual product line within a sale."""
    sale = models.ForeignKey(
        Sale, on_delete=models.CASCADE,
        verbose_name='Venda', related_name='items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT,
        verbose_name='Produto', related_name='sale_items'
    )
    quantity = models.PositiveIntegerField('Quantidade')

    class Meta:
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'
        unique_together = [['sale', 'product']]

    def __str__(self):
        return f'{self.quantity}x {self.product.code}'

    @property
    def subtotal(self):
        return self.quantity * self.product.unit_price
