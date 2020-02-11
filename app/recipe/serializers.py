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
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            Ingredient.objects.create(recipe=recipe, **ingredient)

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.save()
        instance.ingredients.all().delete()

        for ingredient in ingredients:
            instance.ingredients.add(
                Ingredient.objects.create(**ingredient, recipe_id=instance.id))

        return instance
