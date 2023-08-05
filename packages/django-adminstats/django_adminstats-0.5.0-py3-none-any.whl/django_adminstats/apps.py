from django.apps import AppConfig


class Config(AppConfig):
    name = 'django_adminstats'
    verbose_name = 'Statistics Charting'

    def ready(self):
        pass
