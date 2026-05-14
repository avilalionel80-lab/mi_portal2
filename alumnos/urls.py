from django.urls import path
from . import views

app_name = 'alumnos'
urlpatterns = [
    path('login/', views.alumno_login, name='login'),
    path('logout/', views.alumno_logout, name='logout'),
]