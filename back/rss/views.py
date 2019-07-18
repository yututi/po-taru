from .feeder import feedScheduler, feeder
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers, viewsets, mixins
from urllib import request
from bs4 import BeautifulSoup
from .models import Article, RssInfo
from collections import namedtuple
import feedparser
from datetime import datetime
from time import mktime
import pytz
from urllib.parse import urlparse
from back.settings_common import TIME_ZONE

# Create your views here.
local_tz = pytz.timezone(TIME_ZONE)


class ArticleFetchParamSerializer(serializers.Serializer):
    top = serializers.IntegerField(allow_null=True, default=20)
    rssIds = serializers.ListField(
        child=serializers.IntegerField(),
        allow_empty=True,
        default=[]
    )


class RssInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssInfo
        exclude = ['user']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class ArticleView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, req):
        serializer = ArticleFetchParamSerializer(data=req.query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        top = params["top"]

        if not params["rssIds"]:
            print('from user')
            rssInfos = RssInfo.objects.filter(user=1)
        else:
            print('from param')
            rssInfos = RssInfo.objects.filter(pk__in=params["rssIds"])

        articles = Article.objects.filter(
            site__in=[rss.id for rss in rssInfos]).order_by("date")[:top]

        return Response({"rssInfos": [RssInfoSerializer(rssInfo).data for rssInfo in rssInfos],
                         "articles": [ArticleSerializer(article).data for article in articles]})


class RssCreateParamSerializer(serializers.Serializer):
    url = serializers.URLField()


class RssView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, req):
        serializer = RssCreateParamSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # rssの妥当性検証
        try:
            # 当該サイトからサイト名、rss取得用urlを受け取る。
            req4toppage = request.Request(url=data["url"], headers={
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", # リファラを偽装しておかないと403返してくる奴がいる
            })

            soup = BeautifulSoup(request.urlopen(req4toppage), features="html.parser")
            site_name = soup.find("title").text
            linkUrl = soup.find('link', attrs={'type': 'application/rss+xml', 'href': True})["href"]

            if not _is_abs_url(linkUrl):
                parsed_uri = urlparse(data["url"])
                linkUrl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            # すでに存在している場合
            alreadyExistsOne: RssInfo = RssInfo.objects.filter(
                url=linkUrl).first()

            if alreadyExistsOne is not None:
                alreadyExistsOne.user.add(req.user)
                alreadyExistsOne.save()
                return Response(RssInfoSerializer(alreadyExistsOne).data)

            rssInfo = RssInfo(
                url=linkUrl, last_updated=datetime.min, site_name=site_name)

            feeder.feedOne(rssInfo)
            rssInfo.last_updated = datetime.now()

            rssInfo.save()
            rssInfo.user.add(req.user)

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response(data={"message": "RSS情報を取得できませんでした。"}, status=400)

        return Response(RssInfoSerializer(rssInfo).data)


def _is_abs_url(url: str):
    return bool(urlparse(url).netloc)
