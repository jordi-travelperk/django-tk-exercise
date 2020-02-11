from django.test import TestCase
from core import models


class ModelTests(TestCase):

    def test_ingredient_str(self):
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put in the ove',
        )
        ingredient = models.Ingredient.objects.create(
            recipe=recipe,
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            name='Pizza',
            description='Put in the ove',
        )

        self.assertEqual(str(recipe), recipe.name)
