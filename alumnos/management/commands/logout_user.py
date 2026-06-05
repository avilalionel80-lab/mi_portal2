from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    help = 'Cierra todas las sesiones activas de un usuario'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario (DNI)')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'Usuario "{username}" no existe.')

        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        count = 0
        for session in sessions:
            data = session.get_decoded()
            if str(user.pk) == str(data.get('_auth_user_id')):
                session.delete()
                count += 1

        self.stdout.write(self.style.SUCCESS(
            f'Sesiones cerradas para "{username}": {count} eliminada(s).'
        ))
