from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Alumno
from .forms import LoginForm


def alumno_login(request):
    """Vista de login con soporte para 'Recordarme' y redirección por rol."""
    
    # Si el usuario ya está autenticado, redirigir según su rol
    if request.user.is_authenticated:
        return _redirect_by_role(request.user)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            email = form.cleaned_data['email']
            remember = form.cleaned_data.get('remember_me', False)
            
            # Autenticar usando el backend personalizado
            user = authenticate(request, dni=dni, email=email)
            
            if user is not None:
                login(request, user)
                
                # Obtener el objeto Alumno para acceder a es_admin
                try:
                    alumno = Alumno.objects.get(dni=dni)
                except Alumno.DoesNotExist:
                    alumno = None
                
                # Configurar duración de sesión según "Recordarme"
                if remember:
                    # Extender sesión a 30 días
                    request.session.set_expiry(settings.REMEMBER_COOKIE_AGE)
                    # También generar token de recordatorio
                    if alumno:
                        token = alumno.set_remember_token()
                        response = _redirect_by_role(user)
                        response.set_signed_cookie(
                            'alumno_remember',
                            token,
                            salt='remember_alumno',
                            max_age=settings.REMEMBER_COOKIE_AGE,
                            httponly=True,
                            secure=False,
                        )
                        return response
                else:
                    # Sesión estándar de 24 horas
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                
                return _redirect_by_role(user)
            else:
                form.add_error(None, 'DNI o email incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'alumnos/login.html', {'form': form})


def _redirect_by_role(user):
    """Redirige al usuario según su rol (admin o alumno)."""
    try:
        alumno = Alumno.objects.get(dni=user.username)
        if alumno.es_admin:
            return redirect('admin_dashboard')
    except Alumno.DoesNotExist:
        pass
    
    return redirect('alumno_dashboard')


@login_required(login_url='alumnos:login')
def alumno_home(request):
    """Vista de bienvenida para alumnos."""
    try:
        alumno = Alumno.objects.get(dni=request.user.username)
    except Alumno.DoesNotExist:
        alumno = None
    
    context = {'alumno': alumno}
    return render(request, 'alumnos/alumno_home.html', context)


@login_required(login_url='alumnos:login')
def admin_home(request):
    """Vista de bienvenida para administradores."""
    # Verificar que el usuario sea administrador
    try:
        alumno = Alumno.objects.get(dni=request.user.username)
        if not alumno.es_admin:
            return redirect('alumno_dashboard')
    except Alumno.DoesNotExist:
        return redirect('alumnos:login')
    
    context = {'alumno': alumno}
    return render(request, 'alumnos/admin_home.html', context)


def alumno_logout(request):
    """Cierra la sesión del usuario y limpia cookies de recordatorio."""
    if 'alumno_id' in request.session:
        alumno_id = request.session['alumno_id']
        try:
            alumno = Alumno.objects.get(id=alumno_id)
            alumno.clear_remember_token()
        except Alumno.DoesNotExist:
            pass
    
    logout(request)
    response = redirect('alumnos:login')
    response.delete_cookie('alumno_remember')
    return response
