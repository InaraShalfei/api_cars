from rest_framework import serializers

from .models import Auto, Owner, OwnerAuto
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
    owners = OwnerSerializer(many=True)

    class Meta:
        model = Auto
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners')

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        auto = Auto.objects.create(**validated_data)
        for owner in owners:
            current, status = Owner.objects.get_or_create(
                **owner)
            OwnerAuto.objects.create(
                owner=current, car=auto)
        return auto

    #TODO update method

