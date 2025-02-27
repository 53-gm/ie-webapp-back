from django.apps import AppConfig


class LecturesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lectures"

    def ready(self):
        import lectures.signals
