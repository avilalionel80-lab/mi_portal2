import logging

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import LoginForm
from .models import Alumno

logger = logging.getLogger(__name__)


def _dashboard_for(user):
    """Devuelve el nombre de la URL del panel según el rol del usuario."""
    return "alumnos:admin_dashboard" if getattr(user, "es_admin", False) else "alumnos:alumno_dashboard"


@require_http_methods(["GET", "POST"])
def alumno_login(request):
    """Login de alumnos con soporte para 'Recordarme' y validación de términos."""
    if request.user.is_authenticated:
        return redirect(_dashboard_for(request.user))

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data["dni"]
            email = form.cleaned_data["email"]
            remember = form.cleaned_data["remember_me"]

            user = authenticate(request, dni=dni, email=email)
            if user is not None:
                login(request, user)

                alumno = Alumno.objects.filter(dni=dni).first()
                is_admin = bool(alumno and alumno.es_admin)
                response = redirect("alumnos:admin_dashboard" if is_admin else "alumnos:alumno_dashboard")

                if remember and alumno is not None:
                    request.session.set_expiry(settings.REMEMBER_COOKIE_AGE)
                    token = alumno.set_remember_token()
                    response.set_signed_cookie(
                        "alumno_remember",
                        token,
                        salt="remember_alumno",
                        max_age=settings.REMEMBER_COOKIE_AGE,
                        httponly=True,
                        samesite="Lax",
                        secure=settings.SESSION_COOKIE_SECURE,
                    )
                else:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)

                logger.info("Login OK: dni=%s admin=%s remember=%s", dni, is_admin, remember)
                return response

            logger.warning("Login fallido para dni=%s", dni)
            form.add_error(None, "DNI o email incorrectos.")
    else:
        form = LoginForm()

    return render(request, "alumnos/login.html", {"form": form})


@require_POST
def alumno_logout(request):
    """Cierra la sesión, borra el token de 'recordarme' y la cookie asociada."""
    if request.user.is_authenticated:
        Alumno.objects.filter(dni=request.user.username).update(remember_token=None)

    logout(request)
    response = redirect("alumnos:login")
    response.delete_cookie("alumno_remember")
    return response


@login_required(login_url="alumnos:login")
def post_login_redirect(request):
    """Punto de entrada tras el login social (Google): redirige según el rol."""
    return redirect(_dashboard_for(request.user))


@login_required(login_url="alumnos:login")
def alumno_dashboard(request):
    """Panel de inicio para alumnos."""
    return render(request, "alumnos/alumno_dashboard.html")


@login_required(login_url="alumnos:login")
def admin_dashboard(request):
    """Panel de inicio para administradores."""
    if not getattr(request.user, "es_admin", False):
        return redirect("alumnos:alumno_dashboard")
    return render(request, "alumnos/admin_dashboard.html")
