from decimal import Decimal
from django.db import models
from django.utils import timezone

# Create your models here.

class Alumno(models.Model):
    VINCULO = [
        ('Mamá', 'Mamá'),
        ('Papá', 'Papá'),
        ('Tutor', 'Tutor'),
        ('Hermano', 'Hermano'),
        ('Abuelo', 'Abuelo'),
        ('Tio', 'Tio'),
    ]
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    fecha_alta = models.DateField(default=timezone.now)
    domicilio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
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
    
    def __str__(self):
        return self.apellido + " " + self.nombre + " - (DNI: " + self.dni + ")"
    
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

    class Meta:
        ordering = ['dia', 'hora_inicio']

    def __str__(self):
        estado = "LIBRE" if self.libre else "OCUPADO"
        return f"[{self.sucursal.nombre:<10}] {self.get_dia_display():<10} - {self.hora_inicio.strftime('%H:%M')} a {self.hora_fin.strftime('%H:%M')} hs. - {estado:<10}"
    
class TipoDisciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio_por_hora = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " - " + self.descripcion
    
class Disciplina(models.Model):
    HORAS = [
        (Decimal('0.5'), 'Media Hora'),
        (Decimal('1.0'), 'Una Hora'),
        (Decimal('1.5'), 'Una Hora y Media'),
        (Decimal('2.0'), 'Dos Horas'),
        (Decimal('2.5'), 'Dos Horas y Media'),
        (Decimal('3.0'), 'Tres Horas'),
        (Decimal('3.5'), 'Tres Horas y Media'),
        (Decimal('4.0'), 'Cuatro Horas'),
        (Decimal('4.5'), 'Cuatro Horas y Media'),
        (Decimal('5.0'), 'Cinco Horas'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='disciplinas')
    tipo = models.ForeignKey(TipoDisciplina, on_delete=models.CASCADE, related_name='disciplinas')
    cantidad_horas = models.DecimalField(choices=HORAS, max_digits=2, decimal_places=1)
    horario = models.ManyToManyField(HorarioDisciplina, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return "[" + self.sucursal.nombre + "] " + self.nombre

class Inscripcion(models.Model):
    fecha = models.DateField(default=timezone.now)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.disciplina.nombre + " - " + str(self.fecha) + self.alumno.apellido + " " + self.alumno.nombre
    
class Caja(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='cajas')
    fecha = models.DateField(default=timezone.now)
    saldo = models.IntegerField(default=0)
    cerrada = models.BooleanField(default=False)

    def calcular_saldo(self):
        saldo = 0
        for detalle in self.detalle_caja.all():
            if detalle.categoria.tipo == 'Ingreso' or detalle.categoria.tipo == 'Ajuste':
                saldo += detalle.monto
            else:  # Egreso o Gasto
                saldo -= detalle.monto
        self.saldo = saldo
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:  # solo cuando se crea una nueva caja
            last_caja = Caja.objects.order_by('-fecha').first()
            self.saldo = last_caja.saldo if last_caja else 0
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.fecha) + " - Cerrada: " + str(self.cerrada)

class CategoriaCaja(models.Model):
    TIPOS = [
        ('Ingreso', 'Ingreso'),
        ('Egreso', 'Egreso'),
        ('Gasto', 'Gasto'),
        ('Ajuste', 'Ajuste'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)

    def __str__(self):
        return self.tipo + " - " +self.nombre + " - " + self.descripcion

class DetalleCaja(models.Model):
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, related_name='detalle_caja')
    descripcion = models.CharField(max_length=100)
    monto = models.IntegerField()
    categoria = models.ForeignKey(CategoriaCaja, on_delete=models.CASCADE, related_name='detalle_caja')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.caja.calcular_saldo()

    def __str__(self):
        return str(self.monto) + " - " + self.categoria.nombre + " - " + self.descripcion 