from django.db import models


class Person(models.Model):
    """Abstract base model for people entities."""
    name = models.CharField('Nome', max_length=200)
    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Telefone', max_length=20)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Customer(Person):
    """Customer model."""

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['name']


class Salesperson(Person):
    """Salesperson model."""

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'
        ordering = ['name']
