from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Alumno

class AlumnoBackend(BaseBackend):
    def authenticate(self, request, dni=None, email=None):
        try:
            alumno = Alumno.objects.get(dni=dni, email=email)
        except Alumno.DoesNotExist:
            return None

        # Crear o recuperar un User de Django asociado al alumno
        user, created = User.objects.get_or_create(
            username=alumno.dni,
            defaults={
                'email': alumno.email,
                'first_name': alumno.nombre_completo,
            }
        )
        # Guardar el ID del alumno en la sesión para acceso rápido
        request.session['alumno_id'] = alumno.id
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None