from django import template
from ..models import DetalleCuota
from django.db.models import Sum

register = template.Library()

@register.simple_tag
def total_generado(cuota_id):
    return DetalleCuota.objects.filter(cuota_id=cuota_id).aggregate(Sum('monto'))['monto__sum'] or 0

@register.simple_tag
def total_pagado(cuota_id):
    return DetalleCuota.objects.filter(cuota_id=cuota_id, pagada=True).aggregate(Sum('monto'))['monto__sum'] or 0