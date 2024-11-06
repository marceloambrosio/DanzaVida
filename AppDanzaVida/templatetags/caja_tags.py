from django import template
from ..models import Caja, MovimientoCaja
from django.db.models import Sum, Q

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

@register.simple_tag
def saldo_efectivo_periodo(periodo_id):
    cajas = Caja.objects.filter(periodo_id=periodo_id)
    total_ingresos = total_egresos = 0

    for caja in cajas:
        movimientos_efectivo = caja.detalle_caja.filter(metodo_pago='Efectivo')
        ingresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Ingreso')
        egresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Egreso')
        total_ingresos += ingresos
        total_egresos += egresos

    return total_ingresos - total_egresos

@register.simple_tag
def saldo_transferencia_periodo(periodo_id):
    cajas = Caja.objects.filter(periodo_id=periodo_id)
    total_ingresos = total_egresos = 0

    for caja in cajas:
        movimientos_transferencia = caja.detalle_caja.filter(metodo_pago='Transferencia')
        ingresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Ingreso')
        egresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Egreso')
        total_ingresos += ingresos
        total_egresos += egresos

    return total_ingresos - total_egresos

@register.simple_tag
def saldo_total_periodo(periodo_id):
    efectivo = saldo_efectivo_periodo(periodo_id)
    transferencia = saldo_transferencia_periodo(periodo_id)
    return efectivo + transferencia

@register.simple_tag
def saldo_movimientos_efectivo(caja_id):
    movimientos_efectivo = MovimientoCaja.objects.filter(caja_id=caja_id, metodo_pago='Efectivo')
    ingresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Ingreso')
    egresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Egreso')
    return ingresos - egresos

@register.simple_tag
def saldo_movimientos_transferencia(caja_id):
    movimientos_transferencia = MovimientoCaja.objects.filter(caja_id=caja_id, metodo_pago='Transferencia')
    ingresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Ingreso')
    egresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Egreso')
    return ingresos - egresos

@register.simple_tag
def movimientos_por_sucursal_y_dia(periodo_id):
    cajas = Caja.objects.filter(periodo_id=periodo_id).order_by('fecha', 'sucursal__nombre')
    movimientos_por_sucursal = {}

    for caja in cajas:
        movimientos = caja.detalle_caja.all()
        if caja.sucursal.nombre not in movimientos_por_sucursal:
            movimientos_por_sucursal[caja.sucursal.nombre] = []
        for movimiento in movimientos:
            movimientos_por_sucursal[caja.sucursal.nombre].append({
                'fecha': caja.fecha,
                'categoria': movimiento.categoria.nombre,
                'descripcion': movimiento.descripcion,
                'ingreso': movimiento.monto if movimiento.categoria.tipo == 'Ingreso' else 0,
                'egreso': movimiento.monto if movimiento.categoria.tipo == 'Egreso' else 0,
                'sucursal_id': caja.sucursal.id 
            })

    return movimientos_por_sucursal

@register.simple_tag
def saldo_caja(caja_id):
    caja = Caja.objects.get(id=caja_id)
    ingresos = caja.detalle_caja.filter(categoria__tipo='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
    egresos = caja.detalle_caja.filter(categoria__tipo='Egreso').aggregate(total=Sum('monto'))['total'] or 0
    return ingresos - egresos

@register.simple_tag
def saldo_dia_sucursal(fecha, sucursal_id):
    cajas = Caja.objects.filter(fecha=fecha, sucursal_id=sucursal_id)
    ingresos = cajas.aggregate(total_ingresos=Sum('detalle_caja__monto', filter=Q(detalle_caja__categoria__tipo='Ingreso')))['total_ingresos'] or 0
    egresos = cajas.aggregate(total_egresos=Sum('detalle_caja__monto', filter=Q(detalle_caja__categoria__tipo='Egreso')))['total_egresos'] or 0
    return ingresos - egresos
