import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='WeekdayCommissionRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(
                    choices=[
                        (0, 'Segunda-Feira'), (1, 'Terça-Feira'), (2, 'Quarta-Feira'),
                        (3, 'Quinta-Feira'), (4, 'Sexta-Feira'), (5, 'Sábado'), (6, 'Domingo'),
                    ],
                    unique=True,
                    verbose_name='Dia da Semana'
                )),
                ('min_percentage', models.DecimalField(
                    decimal_places=2, max_digits=5,
                    validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)],
                    verbose_name='Percentual Mínimo (%)'
                )),
                ('max_percentage', models.DecimalField(
                    decimal_places=2, max_digits=5,
                    validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)],
                    verbose_name='Percentual Máximo (%)'
                )),
            ],
            options={
                'verbose_name': 'Regra de Comissão por Dia da Semana',
                'verbose_name_plural': 'Regras de Comissão por Dia da Semana',
                'ordering': ['weekday'],
            },
        ),
    ]
