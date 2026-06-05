from django.urls import path
<<<<<<< HEAD

from . import views

app_name = "alumnos"
urlpatterns = [
    path("login/", views.alumno_login, name="login"),
    path("logout/", views.alumno_logout, name="logout"),
    path("post-login/", views.post_login_redirect, name="post_login"),
    path("portal/alumno/", views.alumno_dashboard, name="alumno_dashboard"),
    path("portal/admin/", views.admin_dashboard, name="admin_dashboard"),
]
=======
from . import views

app_name = 'alumnos'
urlpatterns = [
    path('login/', views.alumno_login, name='login'),
    path('logout/', views.alumno_logout, name='logout'),
    path('portal/alumno/', views.alumno_dashboard, name='alumno_dashboard'),
    path('portal/admin/', views.admin_dashboard, name='admin_dashboard'),
]
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
