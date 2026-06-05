"""Configuración de Gunicorn para mi_portal.

Uso:
    gunicorn -c gunicorn.conf.py config.wsgi:application
"""
import multiprocessing
import os

# Escucha solo en localhost: Cloudflare Tunnel (cloudflared) se conecta a este puerto.
bind = os.environ.get("GUNICORN_BIND", "127.0.0.1:8000")

# Regla habitual: (2 x núcleos) + 1. Ajustable por entorno.
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "sync"

timeout = 60
keepalive = 5

# Logs a stdout/stderr para que los capture journald (systemd).
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOGLEVEL", "info")
