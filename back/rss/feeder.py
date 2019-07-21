from apscheduler.schedulers.background import BackgroundScheduler
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers, serializers
from urllib import request
from bs4 import BeautifulSoup
from .models import Article, RssInfo
from collections import namedtuple
import feedparser
import datetime
from time import mktime
import pytz.exceptions
import pytz
from typing import List
from functools import reduce
from back.settings_common import TIME_ZONE
local_tz = pytz.timezone(TIME_ZONE)
from django.utils import timezone
from .utils import is_abs_url

class Feeder():

    def feed_all(self):
        print("start Feeder.feed_all")
        rssInfos: List[RssInfo] = RssInfo.objects.all()

        allNewArticles: List[Article] = []
        # updatedRssInfos :List[RssInfo] = []
        for rssInfo in rssInfos:
            newArticles: List[Article] = self._feed(rssInfo)
            allNewArticles.extend(newArticles)

            if newArticles:
                latest = reduce(lambda p, n: p if p > n else n, [
                                article.date for article in newArticles])
                rssInfo.last_updated = latest
                # TODO bulk update
                # updatedRssInfos.append(rssInfo)
                rssInfo.save()

        if allNewArticles:
            Article.objects.bulk_create(allNewArticles)

    def feedOne(self, rssInfo: RssInfo):
        newArticles: List[Article] = self._feed(rssInfo)

        if newArticles:
            Article.objects.bulk_create(newArticles)
            latest = reduce(lambda p, n: p if p > n else n, [
                            article.date for article in newArticles])
            rssInfo.last_updated = latest

    def _feed(self, rssInfo: RssInfo) -> List[Article]:
        newArticles: List[Article] = []
        last_updated: datetime.datetime = rssInfo.last_updated

        info = feedparser.parse(rssInfo.url)

        feed = info['feed']
        if 'updated_parsed' in feed:
            updated_struct = info['feed']['updated_parsed']
            if updated_struct is not None:
                print('updated_struct'+str(updated_struct))
                updated = datetime.datetime(*updated_struct[:6], tzinfo=timezone.utc)
                if last_updated > updated:
                    return []

        print('last:'+str(last_updated))
        for idx, entry in enumerate(info['entries']):

            import time
            updated_struct :time.struct_time = entry['updated_parsed']
            if updated_struct is None:
                continue
            updated = datetime.datetime(*updated_struct[:6], tzinfo=timezone.utc)
            if last_updated is not None and last_updated >= updated:
                continue

            print('article:'+str(updated))

            # extract thumbnail from article page.
            soup = BeautifulSoup(request.urlopen(
                entry['link']), features="html.parser")
            img_meta = soup.find(
                'meta', attrs={'property': 'og:image', 'content': True})
            img = ''
            if img_meta is not None:
                img = img_meta['content']

            title = entry['title']
            link = entry['link']
            newArticles.append(Article(site=rssInfo,
                                       description=title,
                                       link=link,
                                       date=updated,
                                       img=img if is_abs_url(img) else ''))
        return newArticles


feeder = Feeder()

feedScheduler = BackgroundScheduler()
feedScheduler.add_job(feeder.feed_all, 'interval', minutes=2)
