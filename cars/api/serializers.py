from rest_framework import serializers

from .models import Auto, Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class AutoSerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(read_only=True, many=True)

    class Meta:
        model = Auto
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners')

