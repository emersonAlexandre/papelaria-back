from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Product(models.Model):
    """Product model with commission percentage."""
    code = models.CharField('Código', max_length=50, unique=True)
    description = models.CharField('Descrição', max_length=300)
    unit_price = models.DecimalField(
        'Valor Unitário',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    commission_percentage = models.DecimalField(
        'Percentual de Comissão (%)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['code']

    def __str__(self):
        return f'{self.code} - {self.description}'
