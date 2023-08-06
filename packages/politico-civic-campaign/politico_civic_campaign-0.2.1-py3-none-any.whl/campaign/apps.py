from django.apps import AppConfig


class CampaignConfig(AppConfig):
    name = 'campaign'

    def ready(self):
        from campaign import signals  # noqa
