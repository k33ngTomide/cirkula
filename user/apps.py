from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'


class MyAppConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals

