from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="alumnos:login")
def home(request):
    # `es_admin` lo adjunta AlumnoAdminMiddleware en cada petición autenticada.
    if getattr(request.user, "es_admin", False):
        return render(request, "core/home_admin.html")
    return render(request, "core/home.html")
