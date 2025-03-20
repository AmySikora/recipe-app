from django.shortcuts import render
from django.views.generic import ListView, DetailView   #to display lists
from .models import Recipe        

# Create your views here.
class RecipeListView(ListView):           #class-based view
   model = Recipe                         #specify model
   template_name = 'recipes/recipes_list.html' 
   
class RecipeDetailView(DetailView):
    model = Recipetemplate_name = 'recipes/detail.html'

def home(request):
    return render(request, 'recipes/recipes_home.html')