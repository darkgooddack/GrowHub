from django.apps import AppConfig
from django.contrib.auth import get_user_model
from growhub.settings import SUPERUSER_NAME, SUPERUSER_PASSWORD


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        User = get_user_model()
        username = SUPERUSER_NAME
        password = SUPERUSER_PASSWORD
        email = f'{username}@example.com'

        if not User.objects.filter(username=username).exists():
            print(f'Создаём superuser {username}')
            User.objects.create_superuser(username=username, email=email, password=password)
