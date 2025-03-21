from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe  # Ensure Recipe is correctly imported
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin

# List View for Recipes
class RecipeListView(LoginRequiredMixin, ListView):
#class-based “protected” view    
    model = Recipe
 #specify model   
    template_name = 'recipes/recipes_list.html'

# Detail View for a Single Recipe
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe  
    template_name = 'recipes/detail.html'

# Home View
def home(request):
    return render(request, 'recipes/recipes_home.html')

#define function-based view - records(records()
def records(request):
   #do nothing, simply display page    
   return render(request, 'recipes/records.html')
