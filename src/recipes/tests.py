from django.urls import reverse
from django.test import TestCase
from recipes.models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=60,
            ingredients="flour, sugar, milk, cocoa powder, eggs, baking powder",
            description="A wonderful chocolate cake recipe."
        )

    def test_recipe_name(self):
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.name, "Chocolate Cake")

    def test_cooking_time(self):
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.cooking_time, 60)

    def test_get_absolute_url(self):
        expected_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)