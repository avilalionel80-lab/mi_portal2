from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from django.shortcuts import render
=======
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alumnos/', include('alumnos.urls')),
<<<<<<< HEAD
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('terminos/', lambda request: render(request, 'alumnos/terminos.html'), name='terminos'),
]
=======
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
]
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
