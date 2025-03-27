from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe

from django.contrib.auth.models import User

class RecipeViewsTest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.recipe = Recipe.objects.create(
            name="Vanilla Cupcake",
            cooking_time=45,
            ingredients="flour, sugar, eggs, vanilla extract, baking powder, butter",
            description="A delicious vanilla cupcake recipe.",
            instructions="Mix ingredients. Bake at 350°F for 25 minutes.",
        )

    def test_home_page_loads(self):
        # Test if the home page loads successfully
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_home.html')

    def test_recipe_list_page_loads(self):
        # Test if the list of recipes loads
        response = self.client.get(reverse('recipes:recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipes_list.html')
        self.assertContains(response, "Vanilla Cupcake")  # Ensure test recipe is present

    def test_recipe_detail_page_loads(self):
        # Test if a single recipe detail page loads correctly
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/detail.html')
        self.assertContains(response, "Vanilla Cupcake")

    def test_recipe_detail_link_on_list_page(self):
        # Test if the link to detail page exists in the list
        list_response = self.client.get(reverse('recipes:recipe_list'))
        detail_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertContains(list_response, f'href="{detail_url}"')

    def test_invalid_recipe_detail_404(self):
        # Test if requesting a non-existent recipe returns a 404 error
        response = self.client.get(reverse('recipes:recipe_detail', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 404)
