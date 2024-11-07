from datetime import date
from django import forms
from django.db.models import Q
from django.forms import CheckboxSelectMultiple, TextInput, NumberInput, EmailInput, DateInput, Select
from .models import MovimientoCaja, CategoriaCaja, Caja, Alumno, TipoDisciplina, HorarioDisciplina, Disciplina, Inscripcion, Cuota, Periodo

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
            'localidad': Select(attrs={'class': 'form-control'}),
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

class TipoDisciplinaForm(forms.ModelForm):
    class Meta:
        model = TipoDisciplina
        fields = ['nombre', 'descripcion', 'precio_clase', 'precio_semana_1', 'precio_semana_2', 'precio_semana_3', 'precio_libre']
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'precio_clase': NumberInput(attrs={'class': 'form-control'}),
            'precio_semana_1': NumberInput(attrs={'class': 'form-control'}),
            'precio_semana_2': NumberInput(attrs={'class': 'form-control'}),
            'precio_semana_3': NumberInput(attrs={'class': 'form-control'}),
            'precio_libre': NumberInput(attrs={'class': 'form-control'}),
        }

class HorarioDisciplinaForm(forms.ModelForm):
    class Meta:
        model = HorarioDisciplina
        fields = ['sucursal', 'dia', 'hora_inicio', 'hora_fin']
        widgets = {
            'sucursal': Select(attrs={'class': 'form-control'}),
            'dia': Select(attrs={'class': 'form-control'}),
            'hora_inicio': TextInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_fin': TextInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = ['nombre', 'descripcion', 'sucursal', 'tipo', 'horario', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre': TextInput(attrs={'class': 'form-control'}),
            'descripcion': TextInput(attrs={'class': 'form-control'}),
            'sucursal': Select(attrs={'class': 'form-control'}),
            'tipo': Select(attrs={'class': 'form-control'}),
            'horario': CheckboxSelectMultiple(),
            'fecha_inicio': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Si estamos editando una disciplina existente
            self.fields['horario'].queryset = HorarioDisciplina.objects.filter(Q(libre=True) | Q(disciplina=self.instance))
        else:  # Si estamos creando una nueva disciplina
            self.fields['horario'].queryset = HorarioDisciplina.objects.filter(libre=True)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        self.save_m2m()
        instance.horas_semanales = sum(horario.cantidad_horas for horario in instance.horario.all())
        instance.save(update_fields=['horas_semanales'])
        return instance

class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['fecha', 'alumno', 'disciplina', 'fecha_inicio']
        widgets = {
            'fecha': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'alumno': Select(attrs={'class': 'form-control'}),
            'disciplina': Select(attrs={'class': 'form-control'}),
            'fecha_inicio': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['anio', 'mes']
        widgets = {
            'anio': NumberInput(attrs={'class': 'form-control'}),
            'mes': Select(attrs={'class': 'form-control'}),
        }

class CuotaForm(forms.ModelForm): 
    class Meta: 
        model = Cuota 
        fields = ['periodo', 'fecha_vencimiento'] 
        widgets = { 'periodo': Select(attrs={'class': 'form-control'}), 'fecha_vencimiento': DateInput(attrs={'class': 'form-control', 'type': 'date'}), }

class GenerarCuotaEspecialForm(forms.Form):
    cuota = forms.ModelChoiceField(queryset=Cuota.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.filter(activa=True), widget=forms.Select(attrs={'class': 'form-control'}))
    monto = forms.DecimalField(max_digits=8, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class CajaForm(forms.ModelForm):
    class Meta:
        model = Caja
        fields = ['sucursal', 'fecha']
        widgets = {
            'sucursal': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control'}),
        }

class CategoriaCajaForm(forms.ModelForm):
    class Meta:
        model = CategoriaCaja
        fields = ['nombre', 'descripcion', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
        }

class MovimientoCajaForm(forms.ModelForm):
    class Meta:
        model = MovimientoCaja
        fields = ['caja', 'descripcion', 'monto', 'categoria', 'metodo_pago']
        widgets = {
            'caja': forms.HiddenInput(),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
        }

class PagoCuotaForm(forms.Form):
    METODOS_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Transferencia', 'Transferencia'),
    ]
    metodo_pago = forms.ChoiceField(choices=METODOS_PAGO, widget=forms.Select(attrs={'class': 'form-control'}))
