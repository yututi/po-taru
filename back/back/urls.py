"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url
from django.shortcuts import render
from .auth import LoginView, LogoutView, AuthView, TestView
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rss.views import ArticleView, RssView
from django.urls import path, include
from django.contrib import admin

# @ensure_csrf_cookie
def index(req):
    return render(req, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/auth', AuthView.as_view()),
    url(r'^api/login', LoginView.as_view()),
    url(r'^api/logout', LogoutView.as_view()),
    url(r'^api/article', ArticleView.as_view()),
    url(r'^api/rss', RssView.as_view()),
    url(r'^api/gen/rss/', include('rss.urls')),
    
    # drf の browsable api 見るときはコメントイン(というかﾛｸﾞｲﾝにこっち使うたい)
    # url(r'^api-auth/', include('rest_framework.urls')) 
]

# histry api fallbackのために最後にマッチングさせる
urlpatterns.append(url(r'^.*$', index))
