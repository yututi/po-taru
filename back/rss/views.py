from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers, serializers
from urllib import request
from bs4 import BeautifulSoup
from .models import Article, RssInfo
from collections import namedtuple
import feedparser
from datetime import datetime
from time import mktime
import pytz
from back.settings_common import TIME_ZONE
# Create your views here.
local_tz = pytz.timezone(TIME_ZONE)

# TODO RSSフィードするのはスケジューラで
class RssView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, req):
        # rssInfos = RssInfo.objects.filter(user=req.user.id)
        rssInfos = RssInfo.objects.filter(user=1) # admin
        # FIXME シリアライザに置き換え
        MetaInfo = namedtuple(
            'ArticleInfo', ['rssId', 'siteName', 'img', 'title', 'link', 'updated'])

        print(rssInfos)
        allMetaInfos = []
        allNewArticles = []
        for rssInfo in rssInfos:
            metaInfos = []
            newArticles = []

            latestOne = Article.objects.filter(
                site=rssInfo.id).order_by('-date')[:1]
            latest: datetime = None
            if len(latestOne) > 0:
                latest = latestOne[0].date

            info = feedparser.parse(rssInfo.url)

            feed = info['feed']
            if 'updated_parsed' in feed:
                updated_struct = info['feed']['updated_parsed']
                updated = datetime.fromtimestamp(
                    mktime(updated_struct), tz=local_tz)
                if latest > updated:
                    print('continue')
                    continue

            for entry in info['entries']:
                updated_struct = entry['updated_parsed']
                if updated_struct is None:
                    continue
                updated = datetime.fromtimestamp(
                    mktime(updated_struct), tz=local_tz)
                print(updated)
                print(latest)
                if latest is not None and latest >= updated:
                    print('continue')
                    continue

                s = BeautifulSoup(request.urlopen(
                    entry['link']), features="html.parser")
                img = s.find('meta', attrs={
                             'property': 'og:image', 'content': True})
                content = ''
                if img is not None:
                    content = img['content']
                title = entry['title']
                link = entry['link']
                newArticles.append(Article(site=rssInfo,
                                           description=title,
                                           link=link,
                                           date=updated,
                                           img=content))

                metaInfos.append(MetaInfo(rssInfo.id, rssInfo.site_name,
                                          content, title, link, updated)._asdict())

            newLen = len(metaInfos)
            if newLen < 20:
                articles = Article.objects.filter(
                    site=rssInfo.id).order_by('date')[:20-newLen]
                for article in articles:
                    metaInfos.append(MetaInfo(rssInfo.id,
                                              rssInfo.site_name,
                                              article.img,
                                              article.description,
                                              article.link,
                                              article.date)._asdict())
            allMetaInfos.extend(metaInfos)
            allNewArticles.extend(newArticles)

        if allNewArticles:
            Article.objects.bulk_create(allNewArticles)

        return Response(allMetaInfos)
