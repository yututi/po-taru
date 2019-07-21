from rest_framework import routers
from .views import RssModelViewSet, RssView
from django.urls import include, path

router = routers.DefaultRouter()
router.register(r'rssInfos', RssModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]