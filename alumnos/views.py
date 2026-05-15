from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from .models import Alumno
from .forms import LoginForm


def alumno_login(request):
    """Vista de login de alumnos con soporte para "Recordarme"."""
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
                
                # Extender la duración de la sesión si se marcó "Recordarme"
                if remember:
                    request.session.set_expiry(settings.REMEMBER_COOKIE_AGE)
                    alumno = Alumno.objects.get(dni=dni)
                    token = alumno.set_remember_token()
                else:
                    request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                
                # Redirigir según el rol del usuario
                if user.es_admin:
                    return redirect('alumnos:admin_dashboard')
                else:
                    return redirect('alumnos:alumno_dashboard')
            else:
                form.add_error(None, 'DNI o email incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'alumnos/login.html', {'form': form})


def alumno_logout(request):
    """Vista de logout que limpia la sesión y cookies."""
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


def alumno_dashboard(request):
    """Panel de inicio para alumnos."""
    if not request.user.is_authenticated:
        return redirect('alumnos:login')
    
    return render(request, 'alumnos/alumno_dashboard.html')


def admin_dashboard(request):
    """Panel de inicio para administradores."""
    if not request.user.is_authenticated:
        return redirect('alumnos:login')
    
    if not request.user.es_admin:
        return redirect('alumnos:alumno_dashboard')
    
    return render(request, 'alumnos/admin_dashboard.html')
