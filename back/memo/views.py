from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import serializers
from .models import Memo
from rest_framework import authentication, permissions, serializers, viewsets, mixins
# Create your views here.


class MemoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Memo
        fields = ['id', 'text', 'last_updated']
    
    def create(self, validated_data):
        user = self.context['request'].user
        text = validated_data['text']
        memo = Memo(user=user, text=text)
        memo.save()
        return memo
    
    def update(self, instance, validated_data):
        instance.text = validated_data['text']
        instance.save()
        return instance

class MemoViewSet(ModelViewSet):
    serializer_class = MemoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Memo.objects.filter(user=1)
        return Memo.objects.filter(user=self.request.user.id)
