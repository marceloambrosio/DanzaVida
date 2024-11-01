from django import template
from ..models import Caja

register = template.Library()

@register.simple_tag
def saldo_efectivo(caja_id):
    caja = Caja.objects.get(id=caja_id)
    movimientos_efectivo = caja.detalle_caja.filter(metodo_pago='Efectivo')
    ingresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Ingreso')
    egresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Egreso')
    return ingresos - egresos

@register.simple_tag
def saldo_transferencia(caja_id):
    caja = Caja.objects.get(id=caja_id)
    movimientos_transferencia = caja.detalle_caja.filter(metodo_pago='Transferencia')
    ingresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Ingreso')
    egresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Egreso')
    return ingresos - egresos

@register.simple_tag
def saldo_total(caja_id):
    return saldo_efectivo(caja_id) + saldo_transferencia(caja_id)
