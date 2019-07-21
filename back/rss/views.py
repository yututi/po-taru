from .feeder import feedScheduler, feeder
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions, serializers, viewsets, mixins
from urllib import request
from bs4 import BeautifulSoup
from .models import Article, RssInfo
from collections import namedtuple
import feedparser
import datetime
from time import mktime
import pytz
from .utils import is_abs_url
from urllib.parse import urlparse

class ArticleFetchParamSerializer(serializers.Serializer):
    page_size = serializers.IntegerField(allow_null=True, default=24)
    page = serializers.IntegerField(allow_null=True, default=0)
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

        query_params = {
            'page': req.query_params.get('page', 0),
            'page_size': req.query_params.get('size', 24),
            'rssIds': req.query_params.getlist('rssIds[]', [])
        }
        serializer = ArticleFetchParamSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        page = params["page"]
        page_size = params["page_size"]
        offset = page * page_size

        if not params["rssIds"]:
            print('from user')
            rssInfos = RssInfo.objects.filter(
                user=req.user.id if req.user.id is not None else 1)
        else:
            print('from param')
            rssInfos = RssInfo.objects.filter(pk__in=params["rssIds"])

        articles = Article.objects.filter(
            site__in=[rss.id for rss in rssInfos]).order_by("-date")[offset:offset+page_size]

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
                # リファラを偽装しておかないと403返してくる奴がいる
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
            })

            soup = BeautifulSoup(request.urlopen(
                req4toppage), features="html.parser")
            site_name = soup.find("title").text
            linkUrl = soup.find(
                'link', attrs={'type': 'application/rss+xml', 'href': True})["href"]

            if not is_abs_url(linkUrl):
                parsed_uri = urlparse(data["url"])
                base = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
                linkUrl = base + linkUrl

            # すでに存在している場合
            alreadyExistsOne: RssInfo = RssInfo.objects.filter(
                url=linkUrl).first()

            if alreadyExistsOne is not None:
                alreadyExistsOne.user.add(req.user)
                alreadyExistsOne.save()
                return Response(RssInfoSerializer(alreadyExistsOne).data)

            # 適当な過去日
            last_updated = datetime.datetime(
                1999, 12, 31, 12, 59, 59, 0, datetime.timezone.utc)
            rssInfo = RssInfo(
                url=linkUrl, last_updated=last_updated, site_name=site_name)

            rssInfo.save()
            feeder.feedOne(rssInfo)
            rssInfo.last_updated = datetime.datetime.now(
                tz=datetime.timezone.utc)

            rssInfo.user.add(req.user)
            rssInfo.save()

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            raise serializers.ValidationError(
                {"messages": ["RSS情報を取得できませんでした。"]})

        return Response(RssInfoSerializer(rssInfo).data)

    def delete(self, req):
        rssIds = req.data['rssIds']
        rssInfos: RssInfo = RssInfo.objects.filter(id__in=rssIds)

        for rssInfo in rssInfos:
            rssInfo.user.remove(req.user)

        return Response()


class RssModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RssInfo
        fields = ['id', 'site_name', 'url', 'last_updated']


class RssModelViewSet(ModelViewSet):
    queryset = RssInfo.objects.all()
    serializer_class = RssModelSerializer
    permission_classes = [permissions.AllowAny]
