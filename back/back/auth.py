from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, parsers, serializers
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

        login_data = LoginSerializer(data=req.data)
        login_data.is_valid(raise_exception=True)

        user = authenticate(
            username=login_data.validated_data["username"],
            password=login_data.validated_data["password"])

        if user is not None:
            login(req, user)
            return Response({'id': user.id, 'username': user.username})

        return Response(status=400, data={"messages":['IDまたはパスワードが違います。']})


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny, )

    @method_decorator(csrf_exempt)
    def post(self, req):
        if req.user.is_authenticated:
            logout(req)
        return Response({})


class AuthView(APIView):
    """
    get the userinfo related to session.
    """

    def get(self, req):
        return Response({'id': req.user.id, 'username': req.user.username})


class TestView(APIView):
    def post(self, req):
        return Response({'message': 'done'})


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=30)


def is_valid_csrf(request):
    reason = CsrfViewMiddleware().process_view(request, None, (), {})
    return False if reason else True
