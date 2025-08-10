from django.apps import AppConfig


class KitchenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kitchen'

    def ready(self):
        import kitchen.signals  # noqa Ensure signals get loaded
