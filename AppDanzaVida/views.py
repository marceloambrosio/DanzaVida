from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime
import calendar, json
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AlumnoForm, TipoDisciplinaForm, HorarioDisciplinaForm, DisciplinaForm, InscripcionForm, CuotaForm, PeriodoForm
from .models import Alumno, TipoDisciplina, HorarioDisciplina, Disciplina, Inscripcion, Cuota, DetalleCuota, Periodo, DetallePeriodo, Asistencia, DetalleAsistencia

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