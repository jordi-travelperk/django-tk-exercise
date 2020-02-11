from rest_framework import serializers

from core.models import Ingredient, Recipe


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serialize a recipe"""
    ingredients = IngredientSerializer(many=True,)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'description', 'ingredients'
        )
        read_only_fields = ('id',)

    def create(self, validated_data):
        recipe = Recipe.objects.create(**validated_data)
        ingredients = validated_data.pop('ingredients')
        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients', None)
        if ingredients is not None:  # if an empty list is passed we need to delete all the ingredients
            instance.ingredients.all().delete()
            for ingredient in ingredients:
                Ingredient.objects.create(recipe=instance, **ingredient)
        Recipe.objects.filter(pk=instance.id).update(**validated_data)

        return instance
