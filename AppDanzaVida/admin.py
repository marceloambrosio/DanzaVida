from django.contrib import admin
from .models import Responsable, Alumno, Sucursal, HorarioDisciplina, TipoDisciplina, Disciplina, Inscripcion, Caja, CategoriaCaja, DetalleCaja

# Register your models here.

class ResponsableAdmin(admin.ModelAdmin):
    search_fields = ('apellido', 'nombre'),
    ordering = ['apellido', 'nombre']

class AlumnoAdmin(admin.ModelAdmin):
    search_fields = ('apellido', 'nombre', 'dni'),
    ordering = ['apellido', 'nombre']

class SucursalAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'direccion', 'localidad'),
    ordering = ['nombre', 'direccion']

class HorarioDisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('dia', 'hora_inicio', 'hora_fin'),
    ordering = ['dia', 'hora_inicio']

class TipoDisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion'),
    ordering = ['nombre']

class DisciplinaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion'),
    ordering = ['nombre']

class InscripcionAdmin(admin.ModelAdmin):
    search_fields = ('fecha', 'alumno', 'disciplina'),
    ordering = ['alumno', 'disciplina', 'fecha']

class CajaAdmin(admin.ModelAdmin):
    search_fields = ('fecha', 'monto'),
    ordering = ['fecha']

class CategoriaCajaAdmin(admin.ModelAdmin):
    search_fields = ('nombre', 'descripcion', 'tipo'),
    ordering = ['nombre']

class DetalleCajaAdmin(admin.ModelAdmin):
    search_fields = ('caja', 'categoria', 'monto'),
    ordering = ['caja', 'categoria']

admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(HorarioDisciplina, HorarioDisciplinaAdmin)
admin.site.register(TipoDisciplina, TipoDisciplinaAdmin)
admin.site.register(Disciplina, DisciplinaAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)
admin.site.register(Caja, CajaAdmin)
admin.site.register(CategoriaCaja, CategoriaCajaAdmin)
admin.site.register(DetalleCaja, DetalleCajaAdmin)