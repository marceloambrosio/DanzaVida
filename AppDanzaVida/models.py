from django.db import models
from django.utils import timezone

# Create your models here.

class Responsable(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.apellido + " " + self.nombre
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    fecha_alta = models.DateField(default=timezone.now)
    domicilio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(max_length=50, blank=True, null=True)
    ficha_medica = models.BooleanField(default=False)
    responsable = models.ManyToManyField(Responsable, blank=True)

    def __str__(self):
        return self.apellido + " " + self.nombre + " - (DNI: " + self.dni + ")"
    
class Sucursal(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre + " - " + self.direccion + " - " + self.localidad
    
class HorarioDisciplina(models.Model):
    dia = models.CharField(max_length=20)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    libre = models.BooleanField(default=True)

    def __str__(self):
        return self.dia + " - " + str(self.hora_inicio) + "-" + str(self.hora_fin)
    
class TipoDisciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    arancel1 = models.PositiveIntegerField(blank=True, null=True)
    arancel2 = models.PositiveIntegerField(blank=True, null=True)
    arancel3 = models.PositiveIntegerField(blank=True, null=True)
    arancel4 = models.PositiveIntegerField(blank=True, null=True)
    arancel5 = models.PositiveIntegerField(blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " - " + self.descripcion
    
class Disciplina(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='disciplinas')
    tipo = models.ForeignKey(TipoDisciplina, on_delete=models.CASCADE, related_name='disciplinas')
    horario = models.ManyToManyField(HorarioDisciplina, blank=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.sucursal.nombre + " - " + self.nombre + " - " + self.horario

class Inscripcion(models.Model):
    fecha = models.DateField(default=timezone.now)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.alumno.apellido + " " + self.alumno.nombre + " - " + self.disciplina.nombre + " - " + str(self.fecha)
    
class Caja(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name='cajas')
    fecha = models.DateField(default=timezone.now)
    saldo = models.IntegerField()
    cerrada = models.BooleanField(default=False)

    def __str__(self):
        return self.fecha + " - Cerrada: " + self.cerrada

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

    def __str__(self):
        return self.monto + " - " + self.tipo + " - " + self.descripcion 