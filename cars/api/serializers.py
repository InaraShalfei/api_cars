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
        fields = ('model', 'color', 'production_year', 'engine_capacity', 'owners', 'vin_code')

    def create(self, validated_data):
        owners = validated_data.pop('owners')
        auto = Auto.objects.create(**validated_data)
        for owner in owners:
            current, status = Owner.objects.get_or_create(
                **owner)
            OwnerAuto.objects.create(
                owner=current, auto=auto)
        return auto

    # def update(self, instance, validated_data):
    #     owners = validated_data.pop('owners')
    #     RecipeIngredient.objects.filter(recipe=instance).delete()
    #     recipe_ingredients = {}
    #     for item in ingredients:
    #         amount = item.pop('amount')
    #         ingredient = item.pop('id')
    #         if ingredient.id not in recipe_ingredients:
    #             recipe_ingredients[ingredient.id] = RecipeIngredient(
    #                 amount=amount,
    #                 ingredient=ingredient,
    #                 recipe=instance)
    #         else:
    #             recipe_ingredients[ingredient.id].amount += amount
    #     for recipe_ingredient in recipe_ingredients.values():
    #         recipe_ingredient.save()
    #     for (key, value) in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     instance.tags.set(tags)
    #     return instance

