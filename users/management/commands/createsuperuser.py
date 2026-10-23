import getpass

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Crea un superusuario usando email como identificador de autenticación."

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            dest='email',
            default=None,
            help='Dirección de correo electrónico del superusuario.',
        )
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='Nombre de usuario (opcional; por defecto se usa el email).',
        )
        parser.add_argument(
            '--password',
            dest='password',
            default=None,
            help='Contraseña del superusuario.',
        )
        parser.add_argument(
            '--noinput',
            action='store_true',
            help='No solicitar entrada interactiva del usuario.',
        )

    def handle(self, *args, **options):
        User = get_user_model()

        email = options.get('email')
        username = options.get('username')
        password = options.get('password')
        noinput = options.get('noinput', False)

        # Obtener email
        if not email:
            if noinput:
                raise CommandError('El correo electrónico es requerido en modo no interactivo.')
            email = input('Dirección de correo electrónico: ')

        # Obtener username (usar email si no se proporciona)
        if not username:
            username = email

        # Obtener contraseña
        if not password:
            if noinput:
                raise CommandError('La contraseña es requerida en modo no interactivo.')
            password = getpass.getpass('Contraseña: ')
            password_confirm = getpass.getpass('Confirmar contraseña: ')
            if password != password_confirm:
                raise CommandError("Los dos campos de contraseña no coinciden.")

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
        except Exception as exc:
            raise CommandError(f'Error al crear el superusuario: {exc}')

        self.stdout.write(self.style.SUCCESS('Superusuario creado correctamente.'))
