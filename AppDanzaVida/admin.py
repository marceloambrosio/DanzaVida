from django.contrib import admin
from .models import Alumno, Sucursal, HorarioDisciplina, TipoDisciplina, Disciplina, Inscripcion, Caja, CategoriaCaja, DetalleCaja

# Register your models here.

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    search_fields = ('apellido', 'nombre', 'dni'),
    ordering = ['apellido', 'nombre']

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'direccion', 'localidad'),
    ordering = ['nombre', 'direccion']

@admin.register(HorarioDisciplina)
class HorarioDisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('dia', 'hora_inicio', 'hora_fin'),
    ordering = ['dia', 'hora_inicio']

@admin.register(TipoDisciplina)
class TipoDisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion'),
    ordering = ['nombre']

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion'),
    ordering = ['nombre']

@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    search_fields = ('fecha', 'alumno', 'disciplina'),
    ordering = ['alumno', 'disciplina', 'fecha']

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    search_fields = ('fecha', 'monto'),
    ordering = ['fecha']

@admin.register(CategoriaCaja)
class CategoriaCajaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion', 'tipo'),
    ordering = ['nombre']

@admin.register(DetalleCaja)
class DetalleCajaAdmin(admin.ModelAdmin):
    search_fields = ('caja', 'categoria', 'monto'),
    ordering = ['caja', 'categoria']