from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .views import *

urlpatterns = [
    path('', RedirectView.as_view(url='/home')),
    path('home/', HomeView.as_view(), name='home'),
    path('alumno_nuevo', login_required(AlumnoCreateView.as_view()), name='alumno_create'),
    path('alumno_list', login_required(AlumnoListView.as_view()), name='alumno_list'),
    path('alumno_update/<int:pk>', login_required(AlumnoUpdateView.as_view()), name='alumno_update'),
    path('alumno_delete/<int:pk>', login_required(AlumnoDeleteView.as_view()), name='alumno_delete'),
]