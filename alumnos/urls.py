from django.urls import path
from . import views

app_name = 'alumnos'
urlpatterns = [
    path('login/', views.alumno_login, name='login'),
    path('logout/', views.alumno_logout, name='logout'),
    path('portal/alumno/', views.alumno_dashboard, name='alumno_dashboard'),
    path('portal/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('accounts/', include('allauth.urls')),
]