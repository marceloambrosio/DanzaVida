from datetime import date
from django import forms
from django.forms import TextInput, NumberInput, EmailInput, DateInput, Select
from .models import DetalleCaja, Caja, Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'dni', 'fecha_nacimiento', 'fecha_alta', 'domicilio', 'localidad', 'telefono', 'email', 'observaciones', 'ficha_medica', 'beca', 'descuento', 'responsable1_nombre', 'responsable1_apellido', 'responsable1_vinculo', 'responsable1_telefono', 'responsable1_email', 'responsable2_nombre', 'responsable2_apellido', 'responsable2_vinculo', 'responsable2_telefono', 'responsable2_email', 'responsable3_nombre', 'responsable3_apellido', 'responsable3_vinculo', 'responsable3_telefono', 'responsable3_email']
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'apellido': TextInput(attrs={'class': 'form-control'}),
            'dni': NumberInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_alta': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'domicilio': TextInput(attrs={'class': 'form-control'}),
            'localidad': TextInput(attrs={'class': 'form-control'}),
            'telefono': NumberInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control', 'oninput': 'this.value = this.value.toLowerCase()'}),
            'observaciones': TextInput(attrs={'class': 'form-control'}),
            'ficha_medica': Select(choices=[(False, 'No'), (True, 'Sí')], attrs={'class': 'form-control','id': 'fica_medica'}),
            'beca': Select(choices=[(False, 'No'), (True, 'Sí')], attrs={'class': 'form-control','id': 'beca'}),
            'descuento': NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 100}),
            'responsable1_nombre': TextInput(attrs={'class': 'form-control', 'id': 'responsable1_nombre'}),
            'responsable1_apellido': TextInput(attrs={'class': 'form-control', 'id': 'responsable1_apellido'}),
            'responsable1_vinculo': Select(attrs={'class': 'form-control', 'id': 'responsable1_vinculo'}),
            'responsable1_telefono': NumberInput(attrs={'class': 'form-control', 'id': 'responsable1_telefono'}),
            'responsable1_email': EmailInput(attrs={'class': 'form-control', 'oninput': 'this.value = this.value.toLowerCase()', 'id': 'responsable1_email'}),
            'responsable2_nombre': TextInput(attrs={'class': 'form-control', 'id': 'responsable2_nombre'}),
            'responsable2_apellido': TextInput(attrs={'class': 'form-control', 'id': 'responsable2_apellido'}),
            'responsable2_vinculo': Select(attrs={'class': 'form-control', 'id': 'responsable2_vinculo'}),
            'responsable2_telefono': NumberInput(attrs={'class': 'form-control', 'id': 'responsable2_telefono'}),
            'responsable2_email': EmailInput(attrs={'class': 'form-control', 'oninput': 'this.value = this.value.toLowerCase()', 'id': 'responsable2_email'}),
            'responsable3_nombre': TextInput(attrs={'class': 'form-control', 'id': 'responsable3_nombre'}),
            'responsable3_apellido': TextInput(attrs={'class': 'form-control', 'id': 'responsable3_apellido'}),
            'responsable3_vinculo': Select(attrs={'class': 'form-control', 'id': 'responsable3_vinculo'}),
            'responsable3_telefono': NumberInput(attrs={'class': 'form-control', 'id': 'responsable3_telefono'}),
            'responsable3_email': EmailInput(attrs={'class': 'form-control', 'oninput': 'this.value = this.value.toLowerCase()', 'id': 'responsable3_email'}),
        }

class DetalleCajaForm(forms.ModelForm):
    class Meta:
        model = DetalleCaja
        fields = ['descripcion', 'monto', 'categoria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['caja'].queryset = Caja.objects.filter(fecha=date.today())
        self.fields['caja'].initial = Caja.objects.get_or_create(fecha=date.today())[0]
