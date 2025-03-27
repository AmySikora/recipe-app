from django.urls import reverse
from django.test import TestCase
from recipes.models import Recipe

class RecipeModelTest(TestCase):
    def setUp(self):
        #Sets up test data for the Recipe model
        self.recipe = Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=60,
            ingredients="flour, sugar, milk, cocoa powder, eggs, baking powder",
            description="A wonderful chocolate cake recipe.",
            instructions="Mix ingredients. Bake at 350°F for 30 minutes.",
        )

    def test_recipe_name(self):
        #Test if the recipe name is saved 
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.name, "Chocolate Cake")

    def test_cooking_time(self):
        #Test if the cooking time is stored
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.cooking_time, 60)

    def test_get_absolute_url(self):
        #Test if get_absolute_url() returns the correct URL
        expected_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)


class RecipeViewsTest(TestCase):
    def setUp(self):
        # Set up test data for the views
        self.recipe = Recipe.objects.create(
            name="Vanilla Cupcake",
            cooking_time=45,
            ingredients="flour, sugar, eggs, vanilla extract, baking powder, butter",
            description="A delicious vanilla cupcake recipe.",
            instructions="Mix ingredients. Bake at 350°F for 25 minutes.",
        )

    def test_home_page_loads(self):
        # Test if the home page loads 
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_recipes_list_page_loads(self):
        # Test if the recipes list page loads 
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')
        self.assertContains(response, "Vanilla Cupcake")  # Ensure recipe appears on list page

    def test_recipe_detail_page_loads(self):
        # Test if the recipe detail page loads 
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertContains(response, "Vanilla Cupcake")  # Ensure recipe name appears on detail page

    def test_recipe_detail_link(self):
        # Test if clicking a recipe in the list leads to the detail page
        list_response = self.client.get(reverse('recipes:recipe_list'))
        detail_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertContains(list_response, f'href="{detail_url}"')  # Check if detail page link exists

    def test_invalid_recipe_detail_page(self):
        # Test if accessing a non-existing recipe detail page returns an error
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
