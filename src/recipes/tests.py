from django.test import TestCase
from recipes.models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUp(self):
        Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=60,
            ingredients="flour, sugar, milk, cocoa powder, eggs, baking powder",
            description="A wonderful choclate cake recipe."
        )

    def test_recipe_name(self):
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.name, "Chocolate Cake")

    def test_cooking_time(self):
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.cooking_time, 60)

    def test_get_absolute_url(self):
       recipe = Recipe.objects.get(id=1)
       #get_absolute_url() should take you to the detail page of recipe #1
       #and load the URL /recipes/list/1
       self.assertEqual(recipe.get_absolute_url(), '/recipes/list/1')