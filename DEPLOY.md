# Despliegue en Ubuntu Server — Portal cautivo IPF (Omada ER605)

Guía paso a paso para correr **mi_portal** en una VM con **Ubuntu Server**, publicado por
**Cloudflare Tunnel** y usado como **portal cautivo externo** del router **TP-Link Omada ER605**.

Arquitectura:

```
Cliente WiFi ── redirección del ER605 ──▶ Cloudflare (HTTPS)
                                              │  Cloudflare Tunnel (cloudflared)
                                              ▼
                                   Gunicorn 127.0.0.1:8000  (WhiteNoise sirve los estáticos)
                                              │
                                   Django (mi_portal) ── FreeRADIUS (127.0.0.1:1812)
```

Con este esquema **no necesitás nginx ni abrir puertos** en el firewall: el túnel sale desde la VM.

---

## 1. Requisitos en la VM

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
# Opcional, si vas a validar contra RADIUS local:
sudo apt install -y freeradius freeradius-utils
```

## 2. Crear usuario de servicio y clonar el proyecto

```bash
sudo adduser --system --group --home /opt/mi_portal ipf
sudo -u ipf -H bash
cd /opt/mi_portal
git clone <URL_DE_TU_REPO> .
```

## 3. Entorno virtual y dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Configurar variables de entorno

```bash
cp .env.example .env
# Generá una SECRET_KEY real:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
nano .env
```

Mínimo a completar en `.env` para producción:

- `DJANGO_SECRET_KEY` → la clave generada arriba.
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=portal.tudominio.com,127.0.0.1,localhost`
- `CSRF_TRUSTED_ORIGINS=https://portal.tudominio.com`
- `DEBUG_SKIP_RADIUS=False` (si vas a usar RADIUS) y los datos de RADIUS.
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` (si usás login con Google).

> Las cookies seguras y la confianza en el proxy de Cloudflare se activan solas con
> `DJANGO_DEBUG=False`. **No** actives `SECURE_SSL_REDIRECT` detrás de Cloudflare.

## 5. Migraciones, estáticos y superusuario

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

## 6. Probar a mano

```bash
gunicorn -c gunicorn.conf.py config.wsgi:application
# En otra terminal:  curl -I http://127.0.0.1:8000/alumnos/login/
```

Si responde `200`, cortá con `Ctrl+C` y seguí con el servicio.

## 7. Servicio systemd (Gunicorn)

```bash
sudo cp deploy/mi_portal.service /etc/systemd/system/mi_portal.service
# Revisá User/Group/WorkingDirectory dentro del archivo si cambiaste rutas.
sudo systemctl daemon-reload
sudo systemctl enable --now mi_portal
sudo systemctl status mi_portal
journalctl -u mi_portal -f      # ver logs en vivo
```

## 8. Exponer con Cloudflare Tunnel

```bash
# Instalar cloudflared (ver docs oficiales para tu arquitectura)
cloudflared tunnel login
cloudflared tunnel create mi-portal-ipf
cloudflared tunnel route dns mi-portal-ipf portal.tudominio.com

sudo cp deploy/cloudflared-config.example.yml /etc/cloudflared/config.yml
sudo nano /etc/cloudflared/config.yml          # poné el TUNNEL_ID y tu hostname
sudo cloudflared service install
sudo systemctl status cloudflared
```

Probá entrar a `https://portal.tudominio.com/alumnos/login/` desde afuera.

> En Cloudflare activá **SSL/TLS → "Always Use HTTPS"**. Si usás una URL temporal
> `*.trycloudflare.com`, recordá que cambia en cada arranque: agregала a
> `DJANGO_ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` cada vez (mejor un dominio propio).

## 9. Configurar el portal cautivo en Omada (ER605)

En el **Omada Controller**: `Settings → Authentication → Portal`.

- **SSID / red**: la que querés proteger.
- **Authentication Type**: elegí el modelo que vas a usar (ver abajo).
- **Portal page / External URL**: `https://portal.tudominio.com/alumnos/login/`.

Hay dos modelos posibles y conviene decidir **cuál** vas a usar:

1. **External RADIUS Server** (lo más simple con el ER605): el Omada hace la consulta
   RADIUS a FreeRADIUS directamente; el portal externo solo muestra la página de login.
2. **External Portal Server**: el portal (esta app) autentica y luego **avisa al Omada que
   autorice el dispositivo** (MAC del cliente) vía la API del controller.

> ⚠️ **Pendiente importante:** hoy la app valida credenciales (RADIUS + lista blanca) y muestra
> el dashboard, pero **todavía no notifica al Omada/ER605 que habilite el acceso del cliente**
> a Internet (no captura `clientMac`/`redirectUrl` ni hace el callback de autorización). Según
> el modelo que elijas habrá que: (1) confiar en que el ER605 hace el RADIUS, o (2) implementar
> el callback de "authorize" del External Portal de Omada. Decime cuál usás y lo completamos.

## 10. RADIUS (FreeRADIUS) — notas

- El path por defecto del diccionario en Ubuntu es `/usr/share/freeradius/` (ya contemplado).
- Probá la conectividad con `radtest` antes de poner `DEBUG_SKIP_RADIUS=False`.
- En desarrollo (Windows) dejá `DEBUG_SKIP_RADIUS=True` para no depender de RADIUS.

## 11. Actualizar el despliegue

```bash
cd /opt/mi_portal
sudo -u ipf git pull
sudo -u ipf venv/bin/pip install -r requirements.txt
sudo -u ipf venv/bin/python manage.py migrate
sudo -u ipf venv/bin/python manage.py collectstatic --noinput
sudo systemctl restart mi_portal
```

## 12. Checklist de seguridad para producción

- [ ] `DJANGO_DEBUG=False` y `DJANGO_SECRET_KEY` propia (no la de desarrollo).
- [ ] `DJANGO_ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` con tu hostname real.
- [ ] `DEBUG_SKIP_RADIUS=False` (si corresponde) y `RADIUS_SECRET` real.
- [ ] `python manage.py check --deploy` sin advertencias relevantes.
- [ ] `.env` con permisos restringidos: `chmod 600 .env`.
- [ ] La base `db.sqlite3` queda en la VM, **fuera de git** (ya está en `.gitignore`).
- [ ] Backups de `db.sqlite3` (o migración a PostgreSQL si crece el uso).
