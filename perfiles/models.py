from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

PROVEEDORES = [
    ('J', 'Juan'),
    ('F', 'Felipe'),
    ('G', 'Gerardo')
]
HORARIOS = [
    ('8:00 AM - 10:45 AM', '8:00 AM - 10:45 AM'),
    ('11:00 AM - 12:45 PM', '11:00 AM - 12:45 PM'),
    ('2:00 PM - 3:45 PM', '2:00 PM - 3:45 PM'),
    ('4:00 PM - 5:45 PM', '4:00 PM - 5:45 PM')
]

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    web = models.URLField(blank=True)

    def _str_(self):
        return self.usuario.username

def crear_usuario_perfil(sender, instance, **kwargs):
    if created:
        Perfil.objects.create(usuario=instance)

def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.perfil.save()


class Appointments(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments", default=User, blank = False, null=True)
    prov = models.CharField(max_length = 1, choices = PROVEEDORES, default='Juan')
    date = models.DateField(null=True)
    time = models.CharField(max_length = 20, choices = HORARIOS)
    mdl = models.CharField(max_length = 40)
    rzn = models.CharField(max_length = 255)

    def __str__(self):
        return self.mdl
