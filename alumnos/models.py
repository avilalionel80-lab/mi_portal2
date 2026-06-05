<<<<<<< HEAD
import secrets

from django.contrib.auth import get_user_model
from django.db import models

=======
from django.db import models
import secrets
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531

class Alumno(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=150)
    remember_token = models.CharField(max_length=64, null=True, blank=True, unique=True)
<<<<<<< HEAD
    es_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name="Activo en lista blanca")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["nombre_completo"]

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"

    def sync_user(self):
        """Devuelve (creándolo si hace falta) el User de Django vinculado a este alumno.

        El nombre de usuario es SIEMPRE el DNI, de modo que el login por RADIUS,
        el login por Google y los middlewares identifiquen al alumno de la misma forma.
        """
        User = get_user_model()
        user, _ = User.objects.get_or_create(
            username=self.dni,
            defaults={"email": self.email, "first_name": self.nombre_completo},
        )
        return user

    def set_remember_token(self):
        token = secrets.token_urlsafe(32)
        self.remember_token = token
        self.save(update_fields=["remember_token"])
=======
    es_admin = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True, verbose_name="Activo en lista blanca")

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"

    def set_remember_token(self):
        token = secrets.token_urlsafe(32)
        self.remember_token = token
        self.save(update_fields=['remember_token'])
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
        return token

    def clear_remember_token(self):
        self.remember_token = None
<<<<<<< HEAD
        self.save(update_fields=["remember_token"])
=======
        self.save(update_fields=['remember_token'])
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
