import os

from django.apps import AppConfig


class CoinConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coin'

    def ready(self):
        if os.environ.get("RUN_MAIN"):
            # Make sure the $RUNNER coin exists
            from coin.models import Coin

            Coin.objects.get_or_create(
                name='RUNNER',
                symbol='RUN'
            )
