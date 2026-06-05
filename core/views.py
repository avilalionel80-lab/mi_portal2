<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="alumnos:login")
def home(request):
    # `es_admin` lo adjunta AlumnoAdminMiddleware en cada petición autenticada.
    if getattr(request.user, "es_admin", False):
        return render(request, "core/home_admin.html")
    return render(request, "core/home.html")
=======
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from alumnos.models import Alumno

@login_required(login_url='/alumnos/login/')
def home(request):
    # Obtener el alumno asociado al User logueado
    try:
        alumno = Alumno.objects.get(dni=request.user.username)
    except Alumno.DoesNotExist:
        # Si por alguna razón no hay Alumno, mostrar home normal o error
        return render(request, 'core/home.html')

    if alumno.es_admin:
        return render(request, 'core/home_admin.html')
    else:
        return render(request, 'core/home.html')
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
