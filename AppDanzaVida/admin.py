from django.contrib import admin
from .models import Alumno, Sucursal, HorarioDisciplina, TipoDisciplina, Disciplina, Inscripcion, Periodo, DetallePeriodo, Cuota, DetalleCuota, Asistencia, DetalleAsistencia, Caja, CategoriaCaja, DetalleCaja

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

@admin.register(Periodo)
class PeriodoAdmin(admin.ModelAdmin):
    search_fields = ('anio', 'mes'),
    ordering = ['anio', 'mes']

@admin.register(DetallePeriodo)
class DetallePeriodoAdmin(admin.ModelAdmin):
    search_fields = ('periodo', 'dia_nombre', 'dia_numero'),
    ordering = ['periodo', 'dia_numero', 'dia_nombre']

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    search_fields = ('periodo', 'disciplina'),
    ordering = ['periodo', 'disciplina']

@admin.register(DetalleAsistencia)
class DetalleAsistenciaAdmin(admin.ModelAdmin):
    search_fields = ('asistencia', 'detalle_periodo', 'alumno'),
    ordering = ['asistencia', 'detalle_periodo', 'alumno']

@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'fecha_generacion', 'fecha_vencimiento'),
    ordering = ['fecha_generacion', 'fecha_vencimiento']

@admin.register(DetalleCuota)
class DetalleCuotaAdmin(admin.ModelAdmin):
    search_fields = ('cuota', 'alumno', 'disciplina', 'monto'),
    ordering = ['cuota', 'alumno', 'disciplina']

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