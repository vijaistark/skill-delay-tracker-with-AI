from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create or refresh the demo user used for the app test login.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'demo'
        password = 'Demo@12345'

        user = User.objects.filter(username=username).first()
        if user:
            user.set_password(password)
            user.email = user.email or 'demo@example.com'
            user.save(update_fields=['password', 'email'])
            self.stdout.write(self.style.SUCCESS('Demo user already existed; password was refreshed.'))
            return

        User.objects.create_user(
            username=username,
            email='demo@example.com',
            password=password,
        )
        self.stdout.write(self.style.SUCCESS('Demo user created successfully.'))
