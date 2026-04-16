from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.conf import settings
from .models import Alumno

def alumno_login(request):
    if request.method == 'POST':
        dni = request.POST.get('dni')
        email = request.POST.get('email')
        remember = request.POST.get('remember')

        user = authenticate(request, dni=dni, email=email)

        if user is not None:
            login(request, user)
            alumno = Alumno.objects.get(dni=dni)

            if remember:
                token = alumno.set_remember_token()
                response = redirect('home')  # Asegúrate de tener una URL llamada 'home'
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
                return redirect('home')
        else:
            messages.error(request, "DNI o email incorrectos.")

    return render(request, 'alumnos/login.html')

def alumno_logout(request):
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