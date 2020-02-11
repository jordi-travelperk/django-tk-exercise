from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.utils import json

from core.models import Recipe, Ingredient
from recipe.serializers import RecipeSerializer


def sample_ingredient(name='Cinnamon', recipe={'name': 'Some default name recipe'}):
    """Create and return a sample ingredient"""
    return Ingredient.objects.create(name=name, recipe=recipe)


def sample_recipe(**params):
    """Create and return a sample recipe"""
    defaults = {
        'name': 'Pizza',
        'description': 'Put in the ove',
    }
    defaults.update(params)

    return Recipe.objects.create(**defaults)


class RecipeApiTests(TestCase):
    """Test unauthenticated recipe API access"""
    def setUp(self):
        self.client = APIClient()

    def test_create_basic_recipe(self):
        """Test POST create recipe"""
        payload = {
            'name': 'Pizza',
            'description': 'Put in the ove',
            'ingredients': [
                {'name': 'dough'},
                {'name': 'cheese'},
                {'name': 'tomato'}
            ]
        }
        res = self.client.post('/recipes/',
                               content_type='application/json',
                               data=json.dumps(payload))

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        all_recipes = Recipe.objects.all()
        self.assertEqual(len(all_recipes), 1)

        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], getattr(recipe, 'name'))
        self.assertEqual(payload['description'],
                         getattr(recipe, 'description'))

    def test_retrieve_recipes(self):
        """Test GET get all recipes /recipe/"""
        recipe1 = sample_recipe()
        recipe2 = sample_recipe()
        sample_ingredient(name='cheese', recipe=recipe1)
        sample_ingredient(name='tomato', recipe=recipe1)

        res = self.client.get('/recipes/', format="json")

        recipes = Recipe.objects.all().order_by('-id')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

        self.assertIn(recipe1, recipes)
        self.assertIn(recipe2, recipes)

        serializer1 = RecipeSerializer(recipe1)
        serializer2 = RecipeSerializer(recipe2)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)

    def test_get_single_recipe(self):
        """Test GET single recipe by id /recipe/:id/"""
        recipe1 = sample_recipe()
        sample_ingredient(name='cheese', recipe=recipe1)
        sample_ingredient(name='tomato', recipe=recipe1)

        res = self.client.get(f'/recipes/{recipe1.id}/', format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        serializer1 = RecipeSerializer(recipe1)
        self.assertEqual(res.data, serializer1.data)

    def test_detail_recipe_not_found(self):
        """Test GET single recipe not found by recipe id"""
        response = self.client.get('/recipes/99/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_recipe(self):
        """Test DELETE recipe"""
        recipe1 = sample_recipe()
        sample_ingredient(name='cheese', recipe=recipe1)

        recipes_filled = Recipe.objects.all()
        self.assertEquals(len(recipes_filled), 1)

        res = self.client.delete(f'/recipes/{recipe1.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

        recipes_empty = Recipe.objects.all()
        self.assertEquals(len(recipes_empty), 0)

    def test_update_recipe(self):
        """Test PATCH recipe"""
        recipe1 = sample_recipe()
        sample_ingredient(name='cheese', recipe=recipe1)

        payload = {
            'name': 'Pizza 2',
            'description': 'Put it in the oven 2',
            'ingredients': [
                {'name': 'casa-tarradellas'},
                {'name': 'casa-tarradellas-2'},
                {'name': 'casa-tarradellas-3'}
            ]
        }
        res = self.client.patch(f'/recipes/{recipe1.id}/',
                                content_type='application/json',
                                data=json.dumps(payload))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        recipe = Recipe.objects.get(id=res.data['id'])
        self.assertEqual(payload['name'], str(recipe))

        serializer1 = RecipeSerializer(recipe)
        self.assertEqual(payload['name'], serializer1.data['name'])
        self.assertEqual(payload['description'],
                         serializer1.data['description'])
        self.assertEqual(len(serializer1.data['ingredients']), 3)
        self.assertIn(payload['ingredients'][0],
                      serializer1.data['ingredients'])
        self.assertIn(payload['ingredients'][1],
                      serializer1.data['ingredients'])
        self.assertIn(payload['ingredients'][2],
                      serializer1.data['ingredients'])

    def test_search_recipe(self):
        """Test GET search by name"""
        recipe1 = sample_recipe()
        sample_ingredient(name='cheese', recipe=recipe1)

        res = self.client.get('/recipes/?name=Piz', format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)

    def test_search_recipe_not_found(self):
        """Test GET search by name - no expected results"""
        res = self.client.get('/recipes/?name=thisdoesnotexists')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 0)
