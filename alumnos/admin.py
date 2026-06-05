from django.contrib import admin
<<<<<<< HEAD
from .models import Alumno

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre_completo', 'email', 'es_admin', 'is_active')
    list_filter = ('es_admin', 'is_active')
    search_fields = ('dni', 'nombre_completo', 'email')
    actions = ['activar_alumnos', 'desactivar_alumnos']

    def activar_alumnos(self, request, queryset):
        queryset.update(is_active=True)
    activar_alumnos.short_description = "Activar alumnos seleccionados"

    def desactivar_alumnos(self, request, queryset):
        queryset.update(is_active=False)
    desactivar_alumnos.short_description = "Desactivar alumnos seleccionados"

admin.site.register(Alumno, AlumnoAdmin)
=======

# Register your models here.
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
