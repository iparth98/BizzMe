from django.apps import AppConfig


class UserpanelConfig(AppConfig):
    name = 'userpanel'

    def ready(self):
        import userpanel.signals
