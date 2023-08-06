from django.apps import AppConfig


class AristotleExtensionBaseConfig(AppConfig):
    pass


class AristotleMDRConfig(AristotleExtensionBaseConfig):
    name = 'aristotle_mdr'
    verbose_name = "Aristotle Metadata Registry"

    def ready(self):
        from aristotle_mdr import checks
