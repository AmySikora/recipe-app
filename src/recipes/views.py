from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe  

# List View for Recipes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'

# Detail View for a Single Recipe
class RecipeDetailView(DetailView):
    model = Recipe  
    template_name = 'recipes/detail.html'

    def get_context_data(self, **kwargs):  
        context = super().get_context_data(**kwargs)
        
        # Ensure self.object is used correctly
        context['ingredients_list'] = self.object.ingredients.split(", ")
        context['instructions_list'] = self.object.instructions.split(". ")

        return context

# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')
