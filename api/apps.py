from django.apps import AppConfig
from .data import load_blacklist


FILE_NAME = 'data.json'


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        load_blacklist()
