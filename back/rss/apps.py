from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
import os

class RssConfig(AppConfig):
    name = 'rss'

    def ready(self):
        from .feeder import Feeder
        if os.environ.get('RUN_MAIN', None) != 'true':
            feeder = Feeder()
            scheduler = BackgroundScheduler()
            scheduler.add_job(feeder.feed_all, 'interval', minutes=2)
            # scheduler.start()
