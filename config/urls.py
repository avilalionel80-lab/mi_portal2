from django.contrib import admin
from django.urls import path, include
from alumnos import views as alumno_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('alumnos/', include('alumnos.urls')),
    path('portal/alumno/', alumno_views.alumno_home, name='alumno_dashboard'),
    path('portal/admin/', alumno_views.admin_home, name='admin_dashboard'),
    path('', include('core.urls')),
]