from django.db import models
from django.utils import timezone
from datetime import datetime, date
import calendar
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre + " - " + self.codigo_postal + " (ID: " + str(self.id) + ")"

class Alumno(models.Model):
    VINCULO = [
        ('mama', 'Mamá'),
        ('papa', 'Papá'),
        ('tutor', 'Tutor'),
        ('hermano', 'Hermano'),
        ('abuelo', 'Abuelo'),
        ('tio', 'Tio'),
        ('otro', 'Otro'),
    ]
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    fecha_alta = models.DateField(default=timezone.now)
    domicilio = models.CharField(max_length=100)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, related_name='alumnos')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    observaciones = models.CharField(max_length=400, blank=True, null=True)
    ficha_medica = models.BooleanField(default=False)
    beca = models.BooleanField(default=False)
    descuento = models.PositiveIntegerField(blank=True, null=True)
    responsable1_nombre = models.CharField(max_length=50, blank=True, null=True)
    responsable1_apellido = models.CharField(max_length=50, blank=True, null=True)
    responsable1_vinculo = models.CharField(max_length=20, choices=VINCULO, blank=True, null=True)
    responsable1_telefono = models.CharField(max_length=20, blank=True, null=True)
    responsable1_email = models.EmailField(max_length=50, blank=True, null=True)
    responsable2_nombre = models.CharField(max_length=50, blank=True, null=True)
    responsable2_apellido = models.CharField(max_length=50, blank=True, null=True)
    responsable2_vinculo = models.CharField(max_length=20, choices=VINCULO, blank=True, null=True)
    responsable2_telefono = models.CharField(max_length=20, blank=True, null=True)
    responsable2_email = models.EmailField(max_length=50, blank=True, null=True)
    responsable3_nombre = models.CharField(max_length=50, blank=True, null=True)
    responsable3_apellido = models.CharField(max_length=50, blank=True, null=True)
    responsable3_vinculo = models.CharField(max_length=20, choices=VINCULO, blank=True, null=True)
    responsable3_telefono = models.CharField(max_length=20, blank=True, null=True)
    responsable3_email = models.EmailField(max_length=50, blank=True, null=True)
    
    def calcular_edad(self):
        hoy = timezone.now().date()
        return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))

    @property
    def edad(self):
        return self.calcular_edad()
    
    def __str__(self):
        return self.apellido + " " + self.nombre + " - (DNI: " + str(self.dni) + ")"
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + " - " + self.direccion + " - " + self.localidad
    
class HorarioDisciplina(models.Model):
    DIAS = [
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miercoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sabado'),
        ('7', 'Domingo'),
    ]
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='horarios')
    dia = models.CharField(max_length=20, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    libre = models.BooleanField(default=True)
    cantidad_horas = models.DecimalField(max_digits=4, decimal_places=2, default=0.0, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.cantidad_horas = (datetime.combine(date.min, self.hora_fin) - datetime.combine(date.min, self.hora_inicio)).seconds / 3600
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        estado = "LIBRE" if self.libre else "OCUPADO"
        return f"[{self.sucursal.nombre:<10}] {self.get_dia_display():<10} - {self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')} hs. - {estado:<10}"
    
class TipoDisciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio_clase = models.PositiveIntegerField()
    precio_semana_1 = models.PositiveIntegerField()
    precio_semana_2 = models.PositiveIntegerField()
    precio_semana_3 = models.PositiveIntegerField()
    precio_libre = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " - " + self.descripcion
    
class Disciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='disciplinas')
    tipo = models.ForeignKey(TipoDisciplina, on_delete=models.CASCADE, related_name='disciplinas')
    horas_semanales = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    horario = models.ManyToManyField(HorarioDisciplina, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def veces_por_semana(self):
        return self.horario.count()

    def __str__(self):
        return "[" + self.sucursal.nombre + "] " + self.nombre + " (" + self.tipo.nombre + ") - Inicio: " + str(self.fecha_inicio)

class Inscripcion(models.Model):
    fecha = models.DateField(default=timezone.now)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inicio = models.DateField()
    fecha_baja = models.DateField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.disciplina.nombre + " - " + str(self.fecha) + " - " + self.alumno.apellido + " " + self.alumno.nombre
    
class Periodo(models.Model):
    MESES = [
        ('1', 'Enero'),
        ('2', 'Febrero'),
        ('3', 'Marzo'),
        ('4', 'Abril'),
        ('5', 'Mayo'),
        ('6', 'Junio'),
        ('7', 'Julio'),
        ('8', 'Agosto'),
        ('9', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre'),
    ]
    mes = models.CharField(max_length=20, choices=MESES)
    anio = models.PositiveIntegerField(default=timezone.now().year)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda el Periodo primero
        DIAS = [
            ('1', 'Lunes'),
            ('2', 'Martes'),
            ('3', 'Miercoles'),
            ('4', 'Jueves'),
            ('5', 'Viernes'),
            ('6', 'Sabado'),
            ('7', 'Domingo'),
        ]
        _, num_dias = calendar.monthrange(int(self.anio), int(self.mes))

        # Para cada disciplina activa
        for disciplina in Disciplina.objects.filter(activa=True):
            # Crea una nueva Asistencia
            asistencia = Asistencia.objects.create(periodo=self, disciplina=disciplina)

            for dia in range(1, num_dias + 1):
                dia_nombre = DIAS[calendar.weekday(int(self.anio), int(self.mes), dia)][1]

                # Si la disciplina tiene un horario para este día
                if disciplina.horario.filter(dia=str(calendar.weekday(int(self.anio), int(self.mes), dia) + 1)).exists():
                    # Crea un nuevo DetallePeriodo para este día y esta disciplina
                    detalle_periodo = DetallePeriodo.objects.create(
                        periodo=self,
                        dia_nombre=dia_nombre,
                        dia_numero=dia,
                    )

                    # Para cada alumno inscripto en la disciplina y activo
                    for inscripcion in Inscripcion.objects.filter(disciplina=disciplina, activa=True):
                        # Crea un nuevo DetalleAsistencia
                        DetalleAsistencia.objects.create(
                            asistencia=asistencia,
                            detalle_periodo=detalle_periodo,
                            alumno=inscripcion.alumno,
                        )

    def __str__(self):
        return str(self.anio) + " - " + self.get_mes_display()

class DetallePeriodo(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='detalles')
    dia_nombre = models.CharField(max_length=20)
    dia_numero = models.PositiveIntegerField()
    asistencia_tomada = models.BooleanField(default=False)

    def __str__(self):
        return str(self.periodo.anio) + " - " + self.periodo.get_mes_display() + " - " + str(self.dia_numero) + " (" + self.dia_nombre + ")"

class Asistencia(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='asistencias')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='asistencias')

    def __str__(self):
        return self.periodo.__str__() + " - " + self.disciplina.__str__()
    
class DetalleAsistencia(models.Model):
    asistencia = models.ForeignKey(Asistencia, on_delete=models.CASCADE, related_name='detalles')
    detalle_periodo = models.ForeignKey(DetallePeriodo, on_delete=models.CASCADE, related_name='detalles_asistencia')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='detalles_asistencia')
    presente = models.BooleanField(default=False)

    def __str__(self):
        return self.detalle_periodo.__str__() + self.asistencia.disciplina.nombre +" - " + self.alumno.__str__() + " - " + str(self.presente)

class Caja(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='cajas')
    fecha = models.DateField(default=timezone.now)
    cerrada = models.BooleanField(default=False)
    saldo_efectivo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saldo_transferencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_saldo_efectivo(self):
        movimientos_efectivo = self.detalle_caja.filter(metodo_pago='Efectivo')
        ingresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Ingreso')
        egresos = sum(movimiento.monto for movimiento in movimientos_efectivo if movimiento.categoria.tipo == 'Egreso')
        self.saldo_efectivo = ingresos - egresos
        self.save()

    def calcular_saldo_transferencia(self):
        movimientos_transferencia = self.detalle_caja.filter(metodo_pago='Transferencia')
        ingresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Ingreso')
        egresos = sum(movimiento.monto for movimiento in movimientos_transferencia if movimiento.categoria.tipo == 'Egreso')
        self.saldo_transferencia = ingresos - egresos
        self.save()

    def calcular_saldo_total(self):
        return self.saldo_efectivo + self.saldo_transferencia

    def __str__(self):
        return str(self.fecha) + " - Cerrada: " + str(self.cerrada)

class CategoriaCaja(models.Model):
    TIPOS = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return self.tipo + " - " +self.nombre + " - " + self.descripcion

class MovimientoCaja(models.Model):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='detalle_caja')
    descripcion = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(CategoriaCaja, on_delete=models.CASCADE, related_name='detalle_caja')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)

    def __str__(self):
        return str(self.monto) + " - " + self.categoria.nombre + " - " + self.descripcion 
    
@receiver(post_save, sender=MovimientoCaja)
def actualizar_saldos(sender, instance, **kwargs):
    instance.caja.calcular_saldo_efectivo()
    instance.caja.calcular_saldo_transferencia()

@receiver(post_delete, sender=MovimientoCaja)
def actualizar_saldos_despues_de_borrar(sender, instance, **kwargs):
    instance.caja.calcular_saldo_efectivo()
    instance.caja.calcular_saldo_transferencia()

class Cuota(models.Model):
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, related_name='cuotas')
    fecha_generacion = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Guarda la cuota primero

        # Verifica si la cuota ya tiene detalles
        ya_tiene_detalles = self.detalles.exists()

        # Si la cuota no tiene detalles, los genera
        if not ya_tiene_detalles:
            self.generar_detalles()  # Luego genera los detalles

    def generar_detalles(self):
        inscripciones_activas = Inscripcion.objects.filter(activa=True)
        alumnos = {}
        for inscripcion in inscripciones_activas:
            alumno = inscripcion.alumno
            tipo = inscripcion.disciplina.tipo
            veces_por_semana = inscripcion.disciplina.veces_por_semana()
            if alumno not in alumnos:
                alumnos[alumno] = {'tipos': {tipo: veces_por_semana}, 'disciplinas': [inscripcion.disciplina]}
            else:
                if tipo not in alumnos[alumno]['tipos']:
                    alumnos[alumno]['tipos'][tipo] = veces_por_semana
                else:
                    alumnos[alumno]['tipos'][tipo] += veces_por_semana
                alumnos[alumno]['disciplinas'].append(inscripcion.disciplina)

        for alumno, data in alumnos.items():
            monto_total = 0
            descripcion = ''
            for tipo, veces_por_semana in data['tipos'].items():
                if veces_por_semana == 1:
                    monto = tipo.precio_semana_1
                elif veces_por_semana == 2:
                    monto = tipo.precio_semana_2
                elif veces_por_semana == 3:
                    monto = tipo.precio_semana_3
                elif veces_por_semana > 3:
                    monto = tipo.precio_libre
                monto_total += monto
                descripcion += ', '.join([disciplina.nombre for disciplina in data['disciplinas'] if disciplina.tipo == tipo]) + '; '

            detalle = DetalleCuota(cuota=self, alumno=alumno, monto=monto_total, descripcion=descripcion)
            detalle.save()

    def __str__(self):
        return str(self.periodo) + " - " + str(self.fecha_vencimiento)

class DetalleCuota(models.Model):
    cuota = models.ForeignKey(Cuota, on_delete=models.CASCADE, related_name='detalles')
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    pagada = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)
    movimiento_caja = models.OneToOneField(MovimientoCaja, on_delete=models.SET_NULL, related_name='detalle_cuota', null=True, blank=True)

    def __str__(self):
        return f'{self.cuota.periodo} - {self.alumno.nombre} {self.alumno.apellido} - {self.descripcion} - ${self.monto}'