<<<<<<< HEAD
# mi_portal

Portal cautivo del **Instituto Politécnico Formosa** (Django). Autentica alumnos por
**DNI + email** (validación opcional contra **RADIUS**) y por **Google** (allauth) contra una
lista blanca, y los redirige a su panel según el rol.

## Desarrollo local (Windows)

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env        # editá los valores (en dev: DJANGO_DEBUG=True, DEBUG_SKIP_RADIUS=True)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Login de alumnos: http://127.0.0.1:8000/alumnos/login/
- Admin de Django: http://127.0.0.1:8000/admin/

Cargá alumnos desde el admin (`DNI`, `email`, `nombre_completo`, marcá `es_admin`/`is_active`
según corresponda). En desarrollo `DEBUG_SKIP_RADIUS=True` saltea la validación RADIUS.

## Tests

```powershell
python manage.py test
```

## Producción

El despliegue en **Ubuntu Server** (como portal cautivo del **Omada ER605**, publicado con
**Cloudflare Tunnel**) está documentado paso a paso en **[DEPLOY.md](DEPLOY.md)**.

## Configuración

Toda la configuración sensible se lee de variables de entorno (ver **[.env.example](.env.example)**):
clave secreta, debug, hosts permitidos, credenciales de Google y parámetros de RADIUS.
=======
# Mi_portal
>>>>>>> 9b81311266f5c31fcfbb511a3849a1f6652a2531
