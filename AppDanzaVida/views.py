from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .forms import AlumnoForm
from .models import Alumno

# Create your views here.

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class AlumnoCreateView(CreateView):
    model = Alumno
    form_class = AlumnoForm
    template_name = 'alumno/alumno_create.html'
    success_url = reverse_lazy('alumno_list')