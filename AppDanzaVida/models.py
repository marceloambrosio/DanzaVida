from django.db import models
from django.utils import timezone

# Create your models here.

class Alumno(models.Model):
    VINCULO = [
        ('Mamá', 'Mamá'),
        ('Papá', 'Papá'),
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
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miercoles', 'Miercoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sabado', 'Sabado'),
        ('Domingo', 'Domingo'),
    ]
    dia = models.CharField(max_length=20, choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    libre = models.BooleanField(default=True)

    def __str__(self):
        return self.dia + " - " + str(self.hora_inicio) + "-" + str(self.hora_fin)
    
class TipoDisciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    precio_por_hora = models.PositiveIntegerField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " - " + self.descripcion
    
class Disciplina(models.Model):
    HORAS = [
        (0.5, 'Media Hora'),
        (1, 'Una Hora'),
        (1.5, 'Una Hora y Media'),
        (2, 'Dos Horas'),
        (2.5, 'Dos Horas y Media'),
        (3, 'Tres Horas'),
    ]
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='disciplinas')
    tipo = models.ForeignKey(TipoDisciplina, on_delete=models.CASCADE, related_name='disciplinas')
    cantidad_horas = models.FloatField(choices=HORAS)
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