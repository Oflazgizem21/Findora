from django.apps import AppConfig


class KayipEsyaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kayip_esya'

    def ready(self):
        import kayip_esya.signals