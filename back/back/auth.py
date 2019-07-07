from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers
from django.contrib.auth.models import User


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    @method_decorator(ensure_csrf_cookie)
    def post(self, req):
        if req.user.is_authenticated:
            if req.user.username == req.data["username"]:
                return Response({'id': req.user.id, 'username': req.user.username})
            else:
                logout(req)

        user = authenticate(username=req.data["username"], password=req.data["password"])
        if user is not None:
            login(req, user)
            if req.data.get("rememberMe") is False:
                req.session.set_expiry(0)
            return Response({'id': user.id, 'username': user.username})
        else:
            return Response(status=401)

class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )
    @method_decorator(csrf_exempt)
    def post(self, req):
        if req.user.is_authenticated:
            logout(req)
        return Response({})
