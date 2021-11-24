from django.apps import AppConfig


class CorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cors'

    def ready(self) -> None:
        from cors import handler