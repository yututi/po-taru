from django.apps import AppConfig

import os

class RssConfig(AppConfig):
    name = 'rss'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .feeder import feedScheduler
            feedScheduler.start()
