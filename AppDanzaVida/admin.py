from django.contrib import admin
from .models import Localidad, Alumno, Sucursal, HorarioDisciplina, TipoDisciplina, Disciplina, Inscripcion, Periodo, DetallePeriodo, Cuota, DetalleCuota, Asistencia, DetalleAsistencia, Caja, CategoriaCaja, MovimientoCaja
from import_export.admin import ImportExportModelAdmin
from import_export import resources

# Register your models here.

class LocalidadResource(resources.ModelResource):
    class Meta:
        model = Localidad
        import_id_fields = []

@admin.register(Localidad)
class LocalidadAdmin(ImportExportModelAdmin):
    resource_class = LocalidadResource
    pass

class AlumnoResource(resources.ModelResource):
    class Meta:
        model = Alumno
        import_id_fields = []

@admin.register(Alumno)
class AlumnoAdmin(ImportExportModelAdmin):
    resource_class = AlumnoResource
    pass

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

class DisciplinaResource(resources.ModelResource):
    class Meta:
        model = Disciplina
        import_id_fields = []

@admin.register(Disciplina)
class DisciplinaAdmin(ImportExportModelAdmin):
    resource_class = DisciplinaResource
    pass

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
    search_fields = ('cuota', 'alumno', 'monto'),
    ordering = ['cuota', 'alumno']

@admin.register(Caja)
class CajaAdmin(admin.ModelAdmin):
    search_fields = ('fecha', 'monto'),
    ordering = ['fecha']

@admin.register(CategoriaCaja)
class CategoriaCajaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion', 'tipo'),
    ordering = ['nombre']

@admin.register(MovimientoCaja)
class MovimientoCajaAdmin(admin.ModelAdmin):
    search_fields = ('caja', 'categoria', 'monto'),
    ordering = ['caja', 'categoria']

admin.register(Alumno, AlumnoAdmin)
admin.register(Disciplina, DisciplinaAdmin)
admin.register(Localidad, LocalidadAdmin)