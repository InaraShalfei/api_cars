import datetime

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
    usage_years = serializers.SerializerMethodField()

    class Meta:
        model = Auto
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners', 'vin_code', 'usage_years')

    def get_usage_years(self, obj):
        return datetime.datetime.now().year - obj.production_year

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        auto = Auto.objects.create(**validated_data)
        for owner in owners:
            current, status = Owner.objects.get_or_create(
                **owner)
            OwnerAuto.objects.create(
                owner=current, auto=auto)
        return auto

    def update(self, instance, validated_data):
        owners = validated_data.pop('owners')
        for owner in owners:
            current, status = Owner.objects.get_or_create(
                **owner)
            OwnerAuto.objects.create(
                owner=current, auto=instance)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class AutoListSerializer(serializers.ModelSerializer):
    usage_years = serializers.SerializerMethodField()
    class Meta:
        model = Auto
        fields = ('model', 'color', 'engine_capacity', 'usage_years')

    def get_usage_years(self, obj):
        return datetime.datetime.now().year - obj.production_year
