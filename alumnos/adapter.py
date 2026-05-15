from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .models import Alumno

class WhitelistSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        email = sociallogin.account.extra_data.get('email', '').lower()
        try:
            # Verifica que el correo esté en la tabla Alumno y activo
            alumno = Alumno.objects.get(email__iexact=email, is_active=True)
        except Alumno.DoesNotExist:
            raise ImmediateHttpResponse(HttpResponseForbidden('Tu correo no está autorizado.'))

        # Obtiene o crea el usuario local asociado
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email, email=email)
            user.save()

        sociallogin.connect(request, user)