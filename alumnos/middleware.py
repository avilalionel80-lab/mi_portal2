from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Alumno

class RememberAlumnoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
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