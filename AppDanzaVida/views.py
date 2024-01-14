from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import AlumnoForm
from .models import Alumno

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