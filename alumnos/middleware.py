from django.contrib.auth import login

from .models import Alumno


class RememberAlumnoMiddleware:
    """Re-loguea al alumno a partir de la cookie firmada 'alumno_remember'."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
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
