from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', HomeView.as_view(), name='home'),
    path('alumno_create', login_required(AlumnoCreateView.as_view()), name='alumno_create'),
    path('alumno_list', login_required(AlumnoListView.as_view()), name='alumno_list'),
    path('alumno_update/<int:pk>', login_required(AlumnoUpdateView.as_view()), name='alumno_update'),
    path('alumno_delete/<int:pk>', login_required(AlumnoDeleteView.as_view()), name='alumno_delete'),
    path('tipo_disciplina_create', login_required(TipoDisciplinaCreateView.as_view()), name='tipo_disciplina_create'),
    path('tipo_disciplina_list', login_required(TipoDisciplinaListView.as_view()), name='tipo_disciplina_list'),
    path('tipo_disciplina_update/<int:pk>', login_required(TipoDisciplinaUpdateView.as_view()), name='tipo_disciplina_update'),
    path('tipo_disciplina_delete/<int:pk>', login_required(TipoDisciplinaDeleteView.as_view()), name='tipo_disciplina_delete'),
    path('horario_disciplina_create', login_required(HorarioDisciplinaCreateView.as_view()), name='horario_disciplina_create'),
    path('horario_disciplina_list', login_required(HorarioDisciplinaListView.as_view()), name='horario_disciplina_list'),
    path('horario_disciplina_update/<int:pk>', login_required(HorarioDisciplinaUpdateView.as_view()), name='horario_disciplina_update'),
    path('horario_disciplina_delete/<int:pk>', login_required(HorarioDisciplinaDeleteView.as_view()), name='horario_disciplina_delete'),
    path('disciplina_create', login_required(DisciplinaCreateView.as_view()), name='disciplina_create'),
    path('disciplina_list', login_required(DisciplinaListView.as_view()), name='disciplina_list'),
    path('disciplina_update/<int:pk>', login_required(DisciplinaUpdateView.as_view()), name='disciplina_update'),
    path('disciplina_delete/<int:pk>', login_required(DisciplinaDeleteView.as_view()), name='disciplina_delete'),
    path('inscripcion_create', login_required(InscripcionCreateView.as_view()), name='inscripcion_create'),
    path('inscripcion_list', login_required(InscripcionListView.as_view()), name='inscripcion_list'),
    path('inscripcion_update/<int:pk>', login_required(InscripcionUpdateView.as_view()), name='inscripcion_update'),
    path('inscripcion_delete/<int:pk>', login_required(InscripcionDeleteView.as_view()), name='inscripcion_delete'),
]