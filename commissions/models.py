from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


WEEKDAY_CHOICES = [
    (0, 'Segunda-Feira'),
    (1, 'Terça-Feira'),
    (2, 'Quarta-Feira'),
    (3, 'Quinta-Feira'),
    (4, 'Sexta-Feira'),
    (5, 'Sábado'),
    (6, 'Domingo'),
]


class WeekdayCommissionRule(models.Model):
    """
    Configurable commission limits per weekday.
    When a weekday rule exists, commission percentages are clamped
    between min_percentage and max_percentage.
    """
    weekday = models.IntegerField(
        'Dia da Semana',
        choices=WEEKDAY_CHOICES,
        unique=True
    )
    min_percentage = models.DecimalField(
        'Percentual Mínimo (%)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    max_percentage = models.DecimalField(
        'Percentual Máximo (%)',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    class Meta:
        verbose_name = 'Regra de Comissão por Dia da Semana'
        verbose_name_plural = 'Regras de Comissão por Dia da Semana'
        ordering = ['weekday']

    def __str__(self):
        return (
            f'{self.get_weekday_display()} — '
            f'Mín: {self.min_percentage}% / Máx: {self.max_percentage}%'
        )

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.min_percentage > self.max_percentage:
            raise ValidationError(
                'O percentual mínimo não pode ser maior que o máximo.'
            )
