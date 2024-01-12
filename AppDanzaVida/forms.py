from datetime import date
from django import forms
from .models import DetalleCaja, Caja

class DetalleCajaForm(forms.ModelForm):
    class Meta:
        model = DetalleCaja
        fields = ['descripcion', 'monto', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caja'].queryset = Caja.objects.filter(fecha=date.today())
        self.fields['caja'].initial = Caja.objects.get_or_create(fecha=date.today())[0]