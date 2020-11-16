from django.shortcuts import render, redirect


from django.contrib.auth.forms import AuthenticationForm



#from django.views.generic import CreateView
#from django.urls import reverse_lazy
#from perfiles.forms import RegistroForm2

from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from perfiles.forms import RegistroForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import logout as do_logout
from django.contrib.auth import login as do_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import Appointments, Perfil
from .forms import AppointmentForm

#---------------------------------------------
#class RegistroUsuario(CreateView):
    #model = User
    #template_name = "register.html"
    #form_class = RegistroForm
    #success_url = reverse_lazy('login')


#class RegistroAdmin(CreateView):

    #model = User
    #template_name = "registeradmin.html"
    #form_class = RegistroForm2
    #success_url = reverse_lazy('login')

#-------------------------------------------


def begin(request):
    return render(request, "begin.html")


@login_required(login_url ='login')
def welcome(request):
    citas_dict = {}
    for cita in Appointments.objects.all():
        citas_dict[cita.pk] = {
            'pk': cita.pk,
            'date': cita.date,
            'time': cita.time,
            'mdl':  cita.mdl,
            'rzn': cita.rzn,
            'prov': cita.prov,
            'actual_user': cita.user,
            }

    return render(
        request,
        'welcome.html',
        {
            'citas_dict': citas_dict,
        })


@login_required(login_url ='login')
@user_passes_test(lambda user: user.is_staff, login_url='/welcome/')
def welcomeadmin(request):

    citas_dict = {}
    for cita in Appointments.objects.all():
        citas_dict[cita.pk] = {
            'pk': cita.pk,
            'date': cita.date,
            'time': cita.time,
            'mdl':  cita.mdl,
            'rzn': cita.rzn,
            'prov': cita.prov,
            'actual_user': cita.user,
            }
    return render(
        request,
        'welcomeadmin.html',
        {
            'citas_dict': citas_dict,
        })

def register(request):
    form = RegistroForm()
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    form.fields['password2'].help_text = None

    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Registro exitoso ' + user)
            return redirect('/login')

    context = {'form': form}
    return render(request, "register.html", context)


def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                do_login(request, user)
                #if request.user.is_staff==True:
                return redirect('/welcomeadmin')
                #else:
                    #return redirect('/welcome')

            else:
                messages.info(request, 'Nombre de usuario o password INCORRECTOS')

    return render(request, "login.html", {'form':form})



def logout(request):
    do_logout(request)

    return redirect('/')

"""
def create_appointment(request):
    if request.method == 'POST':
        #checkear 10:00 para schedule
        your_name = request.POST['your-name']
        your_phone = request.POST['your-phone']
        your_email = request.POST['your-email']
        your_schedule = request.POST['your-schedule']
        your_time = request.POST['your-time']
        your_message = request.POST['your-message']

        message_name = request.POST['message-name']
        message_email= request.POST['message-email']
        message = request.POST['message']

"""
"""
        #send e-email
        send_mail(
            message_name,
            message,
            message_email,
            ['J26031998@hotmail.com'],
        )
"""
"""
        return render(request, 'create.html', {})
"""

#Esto no sirve, es para desplegar...
"""
def create(request):
    # return HttpResponse('Aquí estamos en create')
    citas_dict = {}
    for cita in Appointments.objects.all():
        citas_dict[cita.user] = {
            'pk': cita.pk,
            'date': cita.date,
            'mdl':  cita.mdl,
            'rzn': cita.rzn,
            'prov': cita.prov,
        }
    return render(
        request,
        'create.html',
        {
            'citas_dict': citas_dict,
        }
    )
"""

@login_required(login_url ='login')
def create(request):
    new_form = AppointmentForm()
    if request.method == 'POST':
        filled_form = AppointmentForm(request.POST)

        # Se puede modificar el is_valid para validar la cita
        if filled_form.is_valid():
            rpv = False
            for _ in Appointments.objects.all():
                if (
                    _.prov == filled_form.cleaned_data['prov'] and
                    _.date == filled_form.cleaned_data['date'] and
                    _.time == filled_form.cleaned_data['time']
                ):
                    rpv = True
            if not rpv:
                new_cita = filled_form.save(commit=False)
                new_cita.save()
                note = (
                    'La cita de {} se creó exitosamente!!\n'
                    'En la fecha: {}'.format(
                        new_cita.user, filled_form.cleaned_data['date']
                    )
                )
            else:
                note = (
                    'La cita del día {} en el horario {} no está '
                    'disponible\n'.format(
                        filled_form.cleaned_data['date'],
                        filled_form.cleaned_data['time']
                    )
                )
        else:
            note = 'INVALID CREATE!!!'
        return render(
            request,
            'create.html',
            {
                'appointmentform': new_form,
                'note': note
            }
        )
    else:
        return render(
            request,
            'create.html',
            {
                'appointmentform': new_form,
            }
        )

@login_required(login_url ='login')
@user_passes_test(lambda user: user.is_staff, login_url='/create/')
def create_admin(request):
    new_form = AppointmentForm()
    if request.method == 'POST':
        filled_form = AppointmentForm(request.POST)

        # Se puede modificar el is_valid para validar la cita
        if filled_form.is_valid():
            rpv = False
            for _ in Appointments.objects.all():
                if (
                    _.prov == filled_form.cleaned_data['prov'] and
                    _.date == filled_form.cleaned_data['date'] and
                    _.time == filled_form.cleaned_data['time']
                ):
                    rpv = True
            if not rpv:
                new_cita = filled_form.save(commit=False)
                new_cita.save()
                note = (
                    'La cita de {} se creó exitosamente!!\n'
                    'En la fecha: {}'.format(
                        new_cita.user, filled_form.cleaned_data['date']
                    )
                )
            else:
                note = (
                    'La cita del día {} en el horario {} no está '
                    'disponible\n'.format(
                        filled_form.cleaned_data['date'],
                        filled_form.cleaned_data['time']
                    )
                )
        else:
            note = 'INVALID CREATE!!!'
        return render(
            request,
            'create.html',
            {
                'appointmentform': new_form,
                'note': note
            }
        )
    else:
        return render(
            request,
            'create.html',
            {
                'appointmentform': new_form,
            }
        )
"""
@login_required(login_url ='login')
def modify(request, pk):
    inst = Appointments.objects.get(id = pk)
    new_form = AppointmentForm(instance = inst)

    if request.method == 'POST':
        filled_form = AppointmentForm(request.POST, instance=inst)
        if filled_form.is_valid():
            new_cita = filled_form.save(commit=False)
            new_cita.save()
            return redirect('../../welcomeadmin/')


    return render(request, 'create_admin.html', {'appointmentform': new_form})
"""

@login_required(login_url ='login')
#@user_passes_test(lambda user: user.is_staff, login_url='/modify/')
def modify_admin(request, pk):
    inst = Appointments.objects.get(id = pk)
    new_form = AppointmentForm(instance = inst)

    if request.method == 'POST':
        filled_form = AppointmentForm(request.POST, instance=inst)
        if filled_form.is_valid():
            new_cita = filled_form.save(commit=False)
            new_cita.save()
            return redirect('../../welcomeadmin/')


    return render(request, 'create_admin.html', {'appointmentform': new_form})


def delete(request, pk):
    inst = Appointments.objects.get(id = pk)
    if request.method == 'POST':
        inst.delete()
        return redirect('../../welcomeadmin/')

    return render(request, 'delete.html', {'item':inst})
