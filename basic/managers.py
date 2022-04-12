from django.db import models
from django.db.models import (Sum, ExpressionWrapper, F, FloatField)


# TODO: Manager customizado.
# Deve ser associado ao manager do model especificado
class SaleItemManager(models.Manager):
    def sold_by_year(self):
        return self.get_queryset().values(
            'sale__date__year'
        ).annotate(
            subtotal=Sum(ExpressionWrapper(F('quantity') * F('product__sale_price'), output_field=FloatField())),
            year=F('sale__date__year')
        ).values(
            'year', 'subtotal'
        ).order_by('-year')
