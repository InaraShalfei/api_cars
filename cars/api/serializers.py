import datetime

import webcolors
from rest_framework import serializers

from .models import Auto, Owner, OwnerAuto
from djoser.serializers import UserSerializer, User

from .choices import CHOICES


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class AutoListField(serializers.StringRelatedField):
    def to_representation(self, value):
        return f'{value.model}, VIN code: {value.vin_code}, color: {value.color}'


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class OwnerSerializer(serializers.ModelSerializer):
    autos = AutoListField(read_only=True, many=True)
    age = serializers.SerializerMethodField()
    nationality = serializers.ChoiceField(choices=CHOICES, allow_blank=False)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'autos', 'date_of_birth', 'nationality', 'age')

    def get_age(self, obj):
        return datetime.datetime.now().year - obj.date_of_birth


class OwnerListSerializer(serializers.ModelSerializer):
    number_of_autos = serializers.SerializerMethodField()

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'number_of_autos')

    def get_number_of_autos(self, obj):
        return obj.autos.count()


class AutoSerializer(serializers.ModelSerializer):
    owners = OwnerListSerializer(many=True, required=False)
    usage_years = serializers.SerializerMethodField()
    color = Hex2NameColor()

    class Meta:
        model = Auto
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners', 'vin_code', 'usage_years')

    def get_usage_years(self, obj):
        return datetime.datetime.now().year - obj.production_year

    def create(self, validated_data):
        if 'owners' not in self.initial_data:
            auto = Auto.objects.create(**validated_data)
            return auto
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
