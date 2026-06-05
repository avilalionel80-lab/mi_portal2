from django.contrib.auth import login
<<<<<<< HEAD

from .models import Alumno


class RememberAlumnoMiddleware:
    """Re-loguea al alumno a partir de la cookie firmada 'alumno_remember'."""

=======
from django.contrib.auth.models import User
from .models import Alumno

class RememberAlumnoMiddleware:
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
<<<<<<< HEAD
            token = request.get_signed_cookie("alumno_remember", default=None, salt="remember_alumno")
            if token:
                try:
                    alumno = Alumno.objects.get(remember_token=token, is_active=True)
                except Alumno.DoesNotExist:
                    pass
                else:
                    login(request, alumno.sync_user(), backend="alumnos.backends.AlumnoBackend")
        return self.get_response(request)


class AlumnoAdminMiddleware:
    """Adjunta `es_admin` al request.user en cada petición autenticada."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            es_admin = (
                Alumno.objects.filter(dni=request.user.username)
                .values_list("es_admin", flat=True)
                .first()
            )
            request.user.es_admin = bool(es_admin)
        return self.get_response(request)
=======
            token = request.get_signed_cookie('alumno_remember', default=None, salt='remember_alumno')
            if token:
                try:
                    alumno = Alumno.objects.get(remember_token=token)
                    user, _ = User.objects.get_or_create(username=alumno.dni, defaults={'email': alumno.email})
                    login(request, user, backend='alumnos.backends.AlumnoBackend')
                    request.session['alumno_id'] = alumno.id
                except Alumno.DoesNotExist:
                    pass
        return self.get_response(request)
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
