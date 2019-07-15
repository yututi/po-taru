from django.apps import AppConfig
import threading
from sched import scheduler
from .tasks import some_long_duration_process
import time

class TaskRepeater:

    def __init__(self):
        self.s = scheduler()
        self.s.run()

    def tick(self, action):
        print('tick')
        # reschedule this function to run again in a minute
        self.s.enter(1, 0, self.tick, (action,))
        action()


class RssConfig(AppConfig):
    name = 'rss'

    def ready(self):
        print('ready')
        TaskRepeater().tick(some_long_duration_process)
