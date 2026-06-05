from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alumnos/', include('alumnos.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('core.urls')),
    path('terminos/', lambda request: render(request, 'alumnos/terminos.html'), name='terminos'),
]