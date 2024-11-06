from django import template
from ..models import Inscripcion

register = template.Library()

@register.simple_tag
def inscriptos_activos(disciplina_id):
    return Inscripcion.objects.filter(disciplina_id=disciplina_id, activa=True).count()
