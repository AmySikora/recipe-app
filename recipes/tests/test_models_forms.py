from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe
from recipes.forms import RecipeSearchForm
from recipes.forms import RecipeForm, CommentForm

class RecipeFormTest(TestCase):
    def test_valid_recipe_form(self):
        form_data = {
            'name': 'Test Soup',
            'cooking_time': 30,
            'ingredients': 'water, salt, vegetables',
            'description': 'A simple soup',
            'instructions': 'Boil everything.'
        }
        form = RecipeForm(data=form_data)
        self.assertTrue(form.is_valid())

class CommentFormTest(TestCase):
    def test_valid_comment_form(self):
        form_data = {
            'text': 'Great recipe!',
            'rating': 4
        }
        form = CommentForm(data=form_data)
        self.assertTrue(form.is_valid())

class RecipeModelTest(TestCase):
    def setUp(self):
        # Sets up test data for the Recipe model
        self.recipe = Recipe.objects.create(
            name="Chocolate Cake",
            cooking_time=60,
            ingredients="flour, sugar, milk, cocoa powder, eggs, baking powder",
            description="A wonderful chocolate cake recipe.",
            instructions="Mix ingredients. Bake at 350°F for 30 minutes.",
        )

    def test_recipe_name(self):
        # Test if the recipe name is correctly saved
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.name, "Chocolate Cake")

    def test_cooking_time(self):
        # Test if the cooking time is stored correctly
        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.cooking_time, 60)

    def test_get_absolute_url(self):
        # Test if get_absolute_url() returns the correct detail view path
        expected_url = reverse('recipes:recipe_detail', kwargs={'pk': self.recipe.pk})
        self.assertEqual(self.recipe.get_absolute_url(), expected_url)

    def test_recipe_str_method(self):
        self.assertEqual(str(self.recipe), "Chocolate Cake")

class RecipeSearchFormTest(TestCase):
    def test_valid_form_data(self):
    # Test valid search term and valid chart_type choice
        form_data = {
            'search_term': 'cake',
            'chart_type': '#1'  # Must match value from CHART_CHOICES
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_blank_form_data(self):
    # Test that form is invalid if chart_type is not selected (it's required)
        form = RecipeSearchForm(data={})
        self.assertFalse(form.is_valid())  
        self.assertIn('chart_type', form.errors)

    def test_invalid_chart_type(self):
        # Test if the form rejects an invalid chart type
        form = RecipeSearchForm(data={'search_term': 'cake', 'chart_type': 'pieeeee'})
        self.assertFalse(form.is_valid())

        # Test for error messages
    def test_form_error_message_for_missing_chart_type(self):
        form = RecipeSearchForm(data={'search_term': 'cake'})
        self.assertFalse(form.is_valid())
        self.assertIn('chart_type', form.errors)
