from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import Appointments



class RegistroForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Nombre de usario',
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo',
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class AppointmentForm(forms.ModelForm):

    class Meta:
        widgets = {'date': DateInput()}
        model = Appointments
        fields = [
            'user',
            'prov',
            'date',
            'time',
            'mdl',
            'rzn',
        ]
        labels = {
            'user': 'Usuario',
            'prov': 'Proveedor',
            'date': 'Fecha',
            'time': 'Horario',
            'mdl': 'Vehículo',
            'rzn': 'Mensaje',
        }
