from django.apps import AppConfig


class BussinessConfig(AppConfig):
    name = 'bussiness'
    def ready(self):
        import bussiness.signals