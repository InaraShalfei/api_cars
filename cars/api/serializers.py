from rest_framework import serializers

from .models import Auto, Owner
from djoser.serializers import UserSerializer, User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class AutoSerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(read_only=True, many=True)

    class Meta:
        model = Auto
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners')

