from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe  # Ensure Recipe is correctly imported

# List View for Recipes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

# Detail View for a Single Recipe
class RecipeDetailView(DetailView):
    model = Recipe  
    template_name = 'recipes/detail.html'

# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')
