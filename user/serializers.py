
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from .models import CirkulaUser


class CirkulaUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CirkulaUser
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'location')


class CirkulaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CirkulaUser
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'location')