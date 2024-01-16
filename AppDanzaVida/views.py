from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AlumnoForm, TipoDisciplinaForm, HorarioDisciplinaForm, DisciplinaForm, InscripcionForm
from .models import Alumno, TipoDisciplina, HorarioDisciplina, Disciplina, Inscripcion

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class AlumnoCreateView(CreateView, PermissionRequiredMixin, ListView):
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
    
class TipoDisciplinaCreateView(CreateView, PermissionRequiredMixin, ListView):
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
    
class HorarioDisciplinaCreateView(CreateView, PermissionRequiredMixin, ListView):
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
    
class DisciplinaCreateView(CreateView, PermissionRequiredMixin, ListView):
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
    
class InscripcionCreateView(CreateView, PermissionRequiredMixin, ListView):
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

class InscripcionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Inscripcion
    success_url = reverse_lazy('inscripcion_list')
    permission_required = 'AppDanzaVida.delete_inscripcion'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)