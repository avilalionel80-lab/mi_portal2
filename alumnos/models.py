from django.db import models
import secrets

class Alumno(models.Model):
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    nombre_completo = models.CharField(max_length=150)
    remember_token = models.CharField(max_length=64, null=True, blank=True, unique=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.dni})"

    def set_remember_token(self):
        token = secrets.token_urlsafe(32)
        self.remember_token = token
        self.save(update_fields=['remember_token'])
        return token

    def clear_remember_token(self):
        self.remember_token = None
        self.save(update_fields=['remember_token'])