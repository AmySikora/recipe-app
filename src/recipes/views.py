from django.shortcuts import render
from django.views.generic import ListView   #to display lists
from .models import Recipe        
# Create your views here.
class RecipeListView(ListView):           #class-based view
   model = Recipe                         #specify model
   template_name = 'recipes/recipes_list.html'    #specify template 

def home(request):
    return render(request, 'recipes/recipes_home.html')