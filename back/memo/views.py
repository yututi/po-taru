from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from .models import Memo
from rest_framework import authentication, permissions, serializers, viewsets, mixins
# Create your views here.


class MemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memo
        fields = ['text', 'last_updated']
        extra_kwargs = {
            'user': {'write_only': True}
        }

class MemoViewSet(ModelViewSet):
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Memo.objects.filter(user=self.request.user.id)
