from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime
from django.template.loader import get_template
from django.http import HttpResponse
from weasyprint import HTML
from decimal import Decimal
import calendar, json
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AlumnoForm, TipoDisciplinaForm, HorarioDisciplinaForm, DisciplinaForm, InscripcionForm, CuotaForm, PagoCuotaForm, PeriodoForm, CajaForm, CategoriaCajaForm, MovimientoCajaForm
from .models import Sucursal, Alumno, TipoDisciplina, HorarioDisciplina, Disciplina, Inscripcion, Cuota, DetalleCuota, Periodo, DetallePeriodo, Asistencia, DetalleAsistencia, Caja, CategoriaCaja, MovimientoCaja

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class AlumnoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumno/alumno_create.html'
    success_url = reverse_lazy('alumno_list')
    permission_required = 'AppDanzaVida.add_alumno'

class AlumnoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Alumno
    template_name = "alumno/alumno_list.html"
    context_object_name = 'alumnos'
    permission_required = 'AppDanzaVida.view_alumno'

class AlumnoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumno/alumno_update.html'
    success_url = reverse_lazy('alumno_list')
    permission_required = 'AppDanzaVida.change_alumno'

class AlumnoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Alumno
    success_url = reverse_lazy('alumno_list')
    permission_required = 'AppDanzaVida.delete_alumno'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
# Vista para listar las disciplinas de un alumno
class AlumnoDisciplinasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Disciplina
    template_name = "alumno/alumno_disciplinas.html" 
    context_object_name = 'alumno_disciplinas'
    permission_required = 'AppDanzaVida.view_disciplina'

    def get_queryset(self):
        self.alumno = get_object_or_404(Alumno, id=self.kwargs['alumno_id'])
        return self.alumno.inscripciones.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alumno'] = self.alumno
        return context

# Vista para listar las cuotas de un alumno
class AlumnoCuotasListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cuota
    template_name = "alumno/alumno_cuotas.html"
    context_object_name = 'alumno_cuotas'
    permission_required = 'AppDanzaVida.view_cuota'

    def get_queryset(self):
        self.alumno = get_object_or_404(Alumno, id=self.kwargs['alumno_id'])
        return self.alumno.detallecuota_set.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alumno'] = self.alumno
        context['detalle_cuota'] = self.alumno.detallecuota_set.first()
        return context
    
class TipoDisciplinaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = TipoDisciplina
    form_class = TipoDisciplinaForm
    template_name = 'disciplina/tipo_disciplina_create.html'
    success_url = reverse_lazy('tipo_disciplina_list')
    permission_required = 'AppDanzaVida.add_tipo_disciplina'

class TipoDisciplinaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TipoDisciplina
    template_name = "disciplina/tipo_disciplina_list.html"
    context_object_name = 'tipos_disciplina'
    permission_required = 'AppDanzaVida.view_tipo_disciplina'

class TipoDisciplinaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = TipoDisciplina
    form_class = TipoDisciplinaForm
    template_name = 'disciplina/tipo_disciplina_update.html'
    success_url = reverse_lazy('tipo_disciplina_list')
    permission_required = 'AppDanzaVida.change_tipo_disciplina'

class TipoDisciplinaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = TipoDisciplina
    success_url = reverse_lazy('tipo_disciplina_list')
    permission_required = 'AppDanzaVida.delete_tipo_disciplina'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class HorarioDisciplinaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = HorarioDisciplina
    form_class = HorarioDisciplinaForm
    template_name = 'disciplina/horario_disciplina_create.html'
    success_url = reverse_lazy('horario_disciplina_list')
    permission_required = 'AppDanzaVida.add_horario_disciplina'

class HorarioDisciplinaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = HorarioDisciplina
    template_name = "disciplina/horario_disciplina_list.html"
    context_object_name = 'horarios_disciplina'
    permission_required = 'AppDanzaVida.view_horario_disciplina'

class HorarioDisciplinaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = HorarioDisciplina
    form_class = HorarioDisciplinaForm
    template_name = 'disciplina/horario_disciplina_update.html'
    success_url = reverse_lazy('horario_disciplina_list')
    permission_required = 'AppDanzaVida.change_horario_disciplina'

class HorarioDisciplinaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = HorarioDisciplina
    success_url = reverse_lazy('horario_disciplina_list')
    permission_required = 'AppDanzaVida.delete_horario_disciplina'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class DisciplinaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'disciplina/disciplina_create.html'
    success_url = reverse_lazy('disciplina_list')
    permission_required = 'AppDanzaVida.add_disciplina'

    def form_valid(self, form):
        response = super().form_valid(form)
        for horario in self.object.horario.all():
            horario.libre = False
            horario.save()
        return response

class DisciplinaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Disciplina
    template_name = "disciplina/disciplina_list.html"
    context_object_name = 'disciplinas'
    permission_required = 'AppDanzaVida.view_disciplina'

class DisciplinaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Disciplina
    form_class = DisciplinaForm
    template_name = 'disciplina/disciplina_update.html'
    success_url = reverse_lazy('disciplina_list')
    permission_required = 'AppDanzaVida.change_disciplina'

    def form_valid(self, form):
        # Guarda los horarios originales antes de la actualización
        original_horarios = set(self.object.horario.all())
        response = super().form_valid(form)
        # Compara los horarios originales con los horarios actualizados
        updated_horarios = set(self.object.horario.all())
        added_horarios = updated_horarios - original_horarios
        removed_horarios = original_horarios - updated_horarios
        # Actualiza el atributo libre de los horarios añadidos y eliminados
        for horario in added_horarios:
            horario.libre = False
            horario.save()
        for horario in removed_horarios:
            horario.libre = True
            horario.save()
        return response
    
class DisciplinaBajaView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'AppDanzaVida.change_disciplina'

    def post(self, request, *args, **kwargs):
        disciplina = get_object_or_404(Disciplina, pk=kwargs['pk'])
        fecha_baja_str = request.POST.get('fecha_baja')
        fecha_baja = datetime.strptime(fecha_baja_str, '%Y-%m-%d').date() if fecha_baja_str else timezone.now()
        disciplina.fecha_fin = fecha_baja
        disciplina.activa = False
        disciplina.save()

        Inscripcion.objects.filter(disciplina=disciplina, activa=True).update(activa=False, fecha_baja=fecha_baja)

        return redirect('disciplina_list')
    
    def form_valid(self, form):
        form.instance.fecha_baja = timezone.now()
        form.instance.activa = False
        if form.is_valid():
            form.save()
        return super().form_valid(form)

class DisciplinaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Disciplina
    success_url = reverse_lazy('disciplina_list')
    permission_required = 'AppDanzaVida.delete_disciplina'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Guarda los horarios antes de la eliminación
        horarios = set(self.object.horario.all())
        response = super().delete(request, *args, **kwargs)
        # Actualiza el atributo libre de los horarios
        for horario in horarios:
            horario.libre = True
            horario.save()
        return response

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# Vista para listar los alumnos inscritos en una disciplina
class DisciplinaAlumnosListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Alumno
    template_name = "disciplina/disciplina_alumnos.html"
    context_object_name = 'disciplina_alumnos'
    permission_required = 'AppDanzaVida.view_alumno'

    def get_queryset(self):
        self.disciplina = get_object_or_404(Disciplina, id=self.kwargs['disciplina_id'])
        return self.disciplina.inscripciones.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disciplina'] = self.disciplina
        return context
    
class InscripcionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'inscripcion/inscripcion_create.html'
    success_url = reverse_lazy('inscripcion_list')
    permission_required = 'AppDanzaVida.add_inscripcion'

class InscripcionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Inscripcion
    template_name = "inscripcion/inscripcion_list.html"
    context_object_name = 'inscripciones'
    permission_required = 'AppDanzaVida.view_inscripcion'

class InscripcionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Inscripcion
    form_class = InscripcionForm
    template_name = 'inscripcion/inscripcion_update.html'
    success_url = reverse_lazy('inscripcion_list')
    permission_required = 'AppDanzaVida.change_inscripcion'

class InscripcionBajaView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Inscripcion
    fields = ['fecha_baja', 'activa']
    permission_required = 'AppDanzaVida.change_inscripcion'

    def form_valid(self, form):
        fecha_baja_str = self.request.POST.get('fecha_baja')
        fecha_baja = datetime.strptime(fecha_baja_str, '%Y-%m-%d').date() if fecha_baja_str else timezone.now()
        form.instance.fecha_baja = fecha_baja
        form.instance.activa = False
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('disciplina_alumnos', kwargs={'disciplina_id': self.object.disciplina.id})

class InscripcionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Inscripcion
    success_url = reverse_lazy('inscripcion_list')
    permission_required = 'AppDanzaVida.delete_inscripcion'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class PeriodoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Periodo
    form_class = PeriodoForm
    template_name = 'periodo/periodo_create.html'
    success_url = reverse_lazy('periodo_list')
    permission_required = 'AppDanzaVida.add_periodo'

class PeriodoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Periodo
    template_name = "periodo/periodo_list.html"
    context_object_name = 'periodos'
    permission_required = 'AppDanzaVida.view_periodo'

class PeriodoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Periodo
    success_url = reverse_lazy('periodo_list')
    permission_required = 'AppDanzaVida.delete_periodo'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

class AsistenciaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Disciplina
    template_name = "asistencia/asistencia_list.html"
    context_object_name = 'disciplinas'
    permission_required = 'AppDanzaVida.view_asistencia'

    def get_queryset(self):
        return Disciplina.objects.filter(activa=True)
    
class AsistenciaDisciplinaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Alumno
    template_name = 'asistencia/asistencia_disciplina_list.html'
    context_object_name = 'alumnos'
    permission_required = 'AppDanzaVida.view_asistenciaalumno'

    def get_queryset(self):
        disciplina = Disciplina.objects.get(id=self.kwargs['disciplina_id'])
        return Alumno.objects.filter(inscripciones__disciplina=disciplina, inscripciones__activa=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        disciplina = Disciplina.objects.get(id=self.kwargs['disciplina_id'])
        context['disciplina'] = disciplina
        detalles_asistencia = DetalleAsistencia.objects.filter(asistencia__disciplina=disciplina)
        fechas = DetallePeriodo.objects.filter(id__in=detalles_asistencia.values_list('detalle_periodo', flat=True)).order_by('periodo__anio', 'periodo__mes', 'dia_numero')
        context['fechas'] = fechas
        filas = []
        for alumno in context['alumnos']:
            detalles = detalles_asistencia.filter(alumno=alumno)
            filas.append({'alumno': alumno, 'detalles': detalles})
        context['filas'] = filas
        return context

@require_POST
def actualizar_asistencias(request):
    data = json.loads(request.body)
    for asistencia_data in data['asistencias']:
        detalle_asistencia = DetalleAsistencia.objects.get(alumno_id=asistencia_data['alumno_id'], detalle_periodo_id=asistencia_data['fecha_id'])
        detalle_asistencia.presente = asistencia_data['presente']
        detalle_asistencia.save()

    return JsonResponse({'status': 'success'})


class CuotaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cuota
    form_class = CuotaForm
    template_name = 'cuota/cuota_create.html'
    success_url = reverse_lazy('cuota_list')
    permission_required = 'AppDanzaVida.add_cuota'

class CuotaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cuota
    template_name = "cuota/cuota_list.html"
    context_object_name = 'cuotas'
    permission_required = 'AppDanzaVida.view_cuota'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detalles = DetalleCuota.objects.all()
        context['total_generado'] = detalles.aggregate(Sum('monto'))['monto__sum'] or 0
        context['total_pagado'] = detalles.filter(pagada=True).aggregate(Sum('monto'))['monto__sum'] or 0
        return context

class CuotaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cuota
    form_class = CuotaForm
    template_name = 'cuota/cuota_update.html'
    success_url = reverse_lazy('cuota_list')
    permission_required = 'AppDanzaVida.change_cuota'

class CuotaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cuota
    success_url = reverse_lazy('cuota_list')
    permission_required = 'AppDanzaVida.delete_cuota'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class DetalleCuotaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = DetalleCuota
    template_name = "cuota/detalle_cuota_list.html"
    context_object_name = 'detalles_cuota'
    permission_required = 'AppDanzaVida.view_detallecuota'

    def get_queryset(self):
        return DetalleCuota.objects.filter(cuota__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cuota'] = Cuota.objects.get(id=self.kwargs['pk'])
        context['sucursales'] = Sucursal.objects.all()
        return context

class DetalleCuotaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = DetalleCuota
    fields = ['monto']
    template_name = 'cuota/detalle_cuota_update.html'
    permission_required = 'AppDanzaVida.change_detallecuota'

    def get_success_url(self):
        return reverse_lazy('detalle_cuota_list', kwargs={'pk': self.object.cuota.id})
    
class DetalleCuotaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = DetalleCuota
    permission_required = 'AppDanzaVida.delete_detallecuota'

    def get_success_url(self):
        return reverse_lazy('detalle_cuota_list', kwargs={'cuota_id': self.object.cuota.id})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
def actualizar_cuotas(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    cuotas = Cuota.objects.filter(periodo=periodo, detalles__pagada=False).distinct()

    cambios = []

    # Verificar y actualizar cuotas existentes
    for cuota in cuotas:
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

            # Verificar si ya existe un DetalleCuota con el mismo alumno
            detalle_existente = DetalleCuota.objects.filter(
                cuota=cuota,
                alumno=alumno
            ).first()

            if detalle_existente:
                # Si existe, actualizar el monto y la descripción si son diferentes
                if detalle_existente.monto != monto_total or detalle_existente.descripcion != descripcion:
                    cambios.append({
                        'alumno': alumno,
                        'cuota': cuota,
                        'monto_anterior': detalle_existente.monto,
                        'monto_nuevo': monto_total,
                        'descripcion_anterior': detalle_existente.descripcion,
                        'descripcion_nueva': descripcion
                    })
            else:
                # Si no existe, crear un nuevo DetalleCuota
                cambios.append({
                    'alumno': alumno,
                    'cuota': cuota,
                    'monto_anterior': None,
                    'monto_nuevo': monto_total,
                    'descripcion_anterior': None,
                    'descripcion_nueva': descripcion
                })

    if request.method == 'POST':
        for cambio in cambios:
            detalle_existente = DetalleCuota.objects.filter(
                cuota=cambio['cuota'],
                alumno=cambio['alumno']
            ).first()

            if detalle_existente:
                detalle_existente.monto = cambio['monto_nuevo']
                detalle_existente.descripcion = cambio['descripcion_nueva']
                detalle_existente.save()
            else:
                detalle = DetalleCuota(
                    cuota=cambio['cuota'],
                    alumno=cambio['alumno'],
                    monto=cambio['monto_nuevo'],
                    descripcion=cambio['descripcion_nueva']
                )
                detalle.save()

        return redirect('cuota_list')

    return redirect('actualizar_cuotas_mostrar', periodo_id=periodo.id)

def actualizar_cuotas_mostrar(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    cuotas = Cuota.objects.filter(periodo=periodo, detalles__pagada=False).distinct()

    cambios = []

    # Verificar y listar cambios en cuotas existentes
    for cuota in cuotas:
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

            # Verificar si ya existe un DetalleCuota con el mismo alumno
            detalle_existente = DetalleCuota.objects.filter(
                cuota=cuota,
                alumno=alumno
            ).first()

            if detalle_existente:
                # Si existe, listar el cambio si el monto o la descripción son diferentes
                if detalle_existente.monto != monto_total or detalle_existente.descripcion != descripcion:
                    cambios.append({
                        'alumno': alumno,
                        'cuota': cuota,
                        'monto_anterior': detalle_existente.monto,
                        'monto_nuevo': monto_total,
                        'descripcion_anterior': detalle_existente.descripcion,
                        'descripcion_nueva': descripcion
                    })
            else:
                # Si no existe, listar como nuevo DetalleCuota
                cambios.append({
                    'alumno': alumno,
                    'cuota': cuota,
                    'monto_anterior': None,
                    'monto_nuevo': monto_total,
                    'descripcion_anterior': None,
                    'descripcion_nueva': descripcion
                })

    return render(request, 'cuota/cuotas_actualizar.html', {'cambios': cambios, 'periodo': periodo})

def actualizar_cuotas_vencimiento_mostrar(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    cuotas_vencidas = Cuota.objects.filter(periodo=periodo, detalles__pagada=False, fecha_vencimiento__lt=timezone.now()).distinct()

    cambios = []

    for cuota in cuotas_vencidas:
        for detalle in cuota.detalles.filter(pagada=False):
            monto_nuevo = round(detalle.monto * Decimal('1.10') / Decimal('100')) * Decimal('100')
            cambios.append({
                'alumno': detalle.alumno,
                'cuota': cuota,
                'monto_anterior': detalle.monto,
                'monto_nuevo': monto_nuevo,
                'descripcion': detalle.descripcion
            })

    return render(request, 'cuota/cuota_vencimiento.html', {'cambios': cambios, 'periodo': periodo})

def actualizar_cuotas_vencimiento(request, periodo_id):
    periodo = get_object_or_404(Periodo, id=periodo_id)
    cuotas_vencidas = Cuota.objects.filter(periodo=periodo, detalles__pagada=False, fecha_vencimiento__lt=timezone.now()).distinct()

    cambios = []

    for cuota in cuotas_vencidas:
        for detalle in cuota.detalles.filter(pagada=False):
            monto_nuevo = round(detalle.monto * Decimal('1.10') / Decimal('100')) * Decimal('100')
            cambios.append({
                'alumno': detalle.alumno,
                'cuota': cuota,
                'monto_anterior': detalle.monto,
                'monto_nuevo': monto_nuevo,
                'descripcion': detalle.descripcion
            })

    if request.method == 'POST':
        for cambio in cambios:
            detalle = DetalleCuota.objects.filter(
                cuota=cambio['cuota'],
                alumno=cambio['alumno']
            ).first()
            if detalle:
                detalle.monto = cambio['monto_nuevo']
                detalle.save()

        return redirect('cuota_list')

    return redirect('actualizar_cuotas_vencimiento_mostrar', periodo_id=periodo.id)

class PagarCuotaView(View):
    def post(self, request, *args, **kwargs):
        detalle_cuota = get_object_or_404(DetalleCuota, id=self.kwargs['pk'])
        metodo_pago = request.POST.get('metodo_pago')
        sucursal_id = request.POST.get('sucursal')
        sucursal = get_object_or_404(Sucursal, id=sucursal_id)

        # Actualizar el valor pagada a True
        detalle_cuota.pagada = True

        # Obtener o crear la Caja con fecha de hoy
        caja, created = Caja.objects.get_or_create(
            fecha=timezone.now().date(),
            sucursal=sucursal
        )

        # Obtener o crear la CategoriaCaja 'Cuota'
        categoria, created = CategoriaCaja.objects.get_or_create(nombre='Cuota')

        # Crear un nuevo MovimientoCaja
        movimiento_caja = MovimientoCaja.objects.create(
            caja=caja,
            descripcion=f'Cuota del mes {detalle_cuota.cuota.periodo.get_mes_display()} de {detalle_cuota.alumno.apellido} {detalle_cuota.alumno.nombre}',
            monto=detalle_cuota.monto,
            categoria=categoria,
            metodo_pago=metodo_pago
        )

        # Asignar el MovimientoCaja al DetalleCuota
        detalle_cuota.movimiento_caja = movimiento_caja
        detalle_cuota.save()

        return redirect(reverse('detalle_cuota_list', kwargs={'pk': detalle_cuota.cuota.id}))
    
class DetalleCuotaFacturaPDFView(View):
    def get(self, request, *args, **kwargs):
        detalle_cuota = get_object_or_404(DetalleCuota, id=self.kwargs['pk'])

        # Renderizar el template con el contexto
        template = get_template('cuota/detalle_cuota_factura.html')
        context = {'detalle_cuota': detalle_cuota}
        html = template.render(context)

        # Generar el PDF
        pdf = HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()

        # Crear la respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=DanzaVida_{detalle_cuota.cuota.periodo.anio}_{detalle_cuota.cuota.periodo.get_mes_display()}.pdf'
        return response
    
class CajaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'caja/caja_create.html'
    success_url = reverse_lazy('caja_list')
    permission_required = 'AppDanzaVida.add_caja'

class CajaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Caja
    template_name = "caja/caja_list.html"
    context_object_name = 'cajas'
    permission_required = 'AppDanzaVida.view_caja'

class CajaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'caja/caja_create.html'
    success_url = reverse_lazy('caja_list')
    permission_required = 'AppDanzaVida.change_caja'

class CajaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Caja
    success_url = reverse_lazy('caja_list')
    permission_required = 'AppDanzaVida.delete_caja'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class CajaPDFView(View):
    def get(self, request, *args, **kwargs):
        caja = get_object_or_404(Caja, id=self.kwargs['pk'])

        # Renderizar el template con el contexto
        template = get_template('caja/caja_pdf.html')
        context = {'caja': caja}
        html = template.render(context)

        # Generar el PDF
        pdf = HTML(string=html).write_pdf()

        # Crear la respuesta
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename=Caja_{caja.sucursal.nombre}_{caja.fecha}.pdf'
        return response
    
class CategoriaCajaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = CategoriaCaja
    form_class = CategoriaCajaForm
    template_name = 'caja/categoria_caja_create.html'
    success_url = reverse_lazy('categoria_caja_list')
    permission_required = 'AppDanzaVida.add_categoriacaja'

class CategoriaCajaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = CategoriaCaja
    template_name = "caja/categoria_caja_list.html"
    context_object_name = 'categorias_caja'
    permission_required = 'AppDanzaVida.view_categoriacaja'

class CategoriaCajaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = CategoriaCaja
    form_class = CategoriaCajaForm
    template_name = 'caja/categoria_caja_create.html'
    success_url = reverse_lazy('categoria_caja_list')
    permission_required = 'AppDanzaVida.change_categoriacaja'

class CategoriaCajaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = CategoriaCaja
    success_url = reverse_lazy('categoria_caja_list')
    permission_required = 'AppDanzaVida.delete_categoriacaja'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
class MovimientoCajaCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MovimientoCaja
    form_class = MovimientoCajaForm
    template_name = 'caja/movimiento_caja_create.html'
    permission_required = 'AppDanzaVida.add_movimientocaja'

    def get_success_url(self):
        return reverse('movimiento_caja_list', args=[self.object.caja.id])
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            data = kwargs['data'].copy()
            data.update({'caja': self.kwargs['caja_id']})
            kwargs['data'] = data
        return kwargs

class MovimientoCajaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MovimientoCaja
    template_name = "caja/movimiento_caja_list.html"
    context_object_name = 'movimientos_caja'
    permission_required = 'AppDanzaVida.view_movimientocaja'

    def get_queryset(self):
        return MovimientoCaja.objects.filter(caja_id=self.kwargs['caja_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caja'] = Caja.objects.get(id=self.kwargs['caja_id'])
        return context

class MovimientoCajaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MovimientoCaja
    form_class = MovimientoCajaForm
    template_name = 'caja/movimiento_caja_update.html'
    success_url = reverse_lazy('movimiento_caja_list')
    permission_required = 'AppDanzaVida.change_movimientocaja'

class MovimientoCajaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MovimientoCaja
    permission_required = 'AppDanzaVida.delete_movimientocaja'

    def get_success_url(self):
        movimiento_caja = get_object_or_404(MovimientoCaja, id=self.kwargs['pk'])
        return reverse_lazy('movimiento_caja_list', kwargs={'caja_id': movimiento_caja.caja.id})

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)