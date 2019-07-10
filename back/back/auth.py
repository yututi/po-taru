from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers
from django.contrib.auth.models import User
from django.middleware.csrf import rotate_token


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, req):
        # check csrf token. because token had been generated when render index.html
        if not is_valid_csrf(req):
            return Response(status=403, data={'message': "csrf token is invalid."})
        if req.user.is_authenticated:
            logout(req)

        user = authenticate(
            username=req.data["username"], password=req.data["password"])
        if user is not None:
            login(req, user)
            return Response({'id': user.id, 'username': user.username})
        else:
            return Response(status=400)


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )

    @method_decorator(csrf_exempt)
    def post(self, req):
        if req.user.is_authenticated:
            logout(req)
        return Response({})


def is_valid_csrf(request):
    reason = CsrfViewMiddleware().process_view(request, None, (), {})
    return False if reason else True
