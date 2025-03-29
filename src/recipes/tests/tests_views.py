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

class SearchViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Add two recipes
        Recipe.objects.create(
            name="Grilled Cheese",
            cooking_time=10,
            ingredients="bread, cheese, butter",
            description="A simple grilled cheese sandwich.",
            instructions="Butter bread, add cheese, grill until golden."
        )
        Recipe.objects.create(
            name="Spaghetti",
            cooking_time=25,
            ingredients="pasta, tomato sauce, basil",
            description="Classic spaghetti with tomato sauce.",
            instructions="Boil pasta, heat sauce, combine."
        )

    def test_search_page_loads(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/search.html')
        self.assertContains(response, "Find a Recipe")

    def test_search_returns_all_recipes_when_blank(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertContains(response, "Grilled Cheese")
        self.assertContains(response, "Spaghetti")

    def test_search_filters_recipes_by_name(self):
        response = self.client.get(reverse('recipes:search'), {'search_term': 'cheese'})
        self.assertContains(response, "Grilled Cheese")
        self.assertNotContains(response, "Spaghetti")

    def test_search_filters_recipes_by_ingredient(self):
        response = self.client.get(reverse('recipes:search'), {'search_term': 'basil'})
        self.assertContains(response, "Spaghetti")
        self.assertNotContains(response, "Grilled Cheese")

    def test_search_view_displays_no_results(self):
        response = self.client.get(reverse('recipes:search'), {'search_term': 'sushi'})
        self.assertContains(response, "No recipes found")
