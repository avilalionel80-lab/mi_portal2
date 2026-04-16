from django.urls import path
from . import views   # <--- Así se importa views desde el mismo paquete

app_name = 'alumnos'
urlpatterns = [
    path('login/', views.alumno_login, name='login'),
    path('logout/', views.alumno_logout, name='logout'),
]