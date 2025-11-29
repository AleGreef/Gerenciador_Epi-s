from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_login'

    def ready(self):
        import app_login.signals

class AppLoginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_login'
