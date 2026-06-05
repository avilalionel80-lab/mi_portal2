import logging

from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User

# Librerías para RADIUS
import pyrad.packet
from pyrad.client import Client
from pyrad.dictionary import Dictionary

from .models import Alumno

logger = logging.getLogger(__name__)


class AlumnoBackend(BaseBackend):
    def authenticate(self, request, dni=None, email=None):
        if not dni or not email:
            return None

        # 1. Validación RADIUS para el ER605 (se omite en desarrollo con DEBUG_SKIP_RADIUS).
        if getattr(settings, "DEBUG_SKIP_RADIUS", False):
            logger.info("DEBUG_SKIP_RADIUS: omitiendo RADIUS para DNI %s", dni)
        elif not self._radius_accepts(dni):
            return None

        # 2. Vinculación con el modelo Alumno local (lista blanca).
        try:
            alumno = Alumno.objects.get(dni=dni, email=email, is_active=True)
        except Alumno.DoesNotExist:
            return None

        # 3. Recuperar (o crear) el User de Django. La sesión la maneja la vista, no el backend.
        return alumno.sync_user()

    def _radius_accepts(self, dni):
        """Consulta al servidor RADIUS si el DNI está autorizado."""
        try:
            srv = Client(
                server=getattr(settings, "RADIUS_SERVER", "127.0.0.1"),
                secret=getattr(settings, "RADIUS_SECRET", b"secret_omada"),
                dict=Dictionary(getattr(settings, "RADIUS_DICT_PATH", "/usr/share/freeradius/dictionary")),
            )

            req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest, User_Name=str(dni))
            req["User-Password"] = req.PwCrypt(str(dni))
            req["NAS-Identifier"] = "ER605-Portal"

            reply = srv.SendPacket(req)
            if reply.code != pyrad.packet.AccessAccept:
                logger.warning("RADIUS Omada: denegado para %s", dni)
                return False
            return True
        except Exception as e:
            logger.error("Error de conexión RADIUS con ER605: %s", e)
            return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
