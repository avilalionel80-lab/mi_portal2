from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponseForbidden

from .models import Alumno


class WhitelistSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Solo permite el login con Google a correos presentes en la lista blanca (Alumno)."""

    def pre_social_login(self, request, sociallogin):
        email = (sociallogin.account.extra_data.get("email") or "").lower()
        if not email:
            raise ImmediateHttpResponse(
                HttpResponseForbidden("No se pudo obtener el correo de tu cuenta de Google.")
            )

        try:
            alumno = Alumno.objects.get(email__iexact=email, is_active=True)
        except Alumno.DoesNotExist:
            raise ImmediateHttpResponse(HttpResponseForbidden("Tu correo no está autorizado."))

        # Si el login social ya está vinculado a un usuario, dejamos que allauth siga su curso.
        if sociallogin.is_existing:
            return

        # Vinculamos al User de Django (username = dni), consistente con el backend RADIUS.
        sociallogin.connect(request, alumno.sync_user())
