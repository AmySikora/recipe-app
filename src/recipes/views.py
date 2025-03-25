from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm  
from .forms import RecipeSearchForm  # Make sure this exists
from .models import Recipe
import pandas as pd

# List View for Recipes (Protected)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    login_url = '/login/'

# Detail View for a Single Recipe (Protected)
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe  
    template_name = 'recipes/detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_list'] = self.object.ingredients.split(", ")
        context['instructions_list'] = self.object.instructions.split("\n")
        return context

# Home View (Public)
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Records View with Form Logic (Protected)
@login_required(login_url='/login/')
def records(request):
    form = RecipeSearchForm(request.POST or None)
    recipe_title = chart_type = None
    recipes_df=None

    if request.method == 'POST':
        if form.is_valid():
            recipe_title = form.cleaned_data.get('recipe_title')
            chart_type = form.cleaned_data.get('chart_type')

            #apply filter to extract data
            qs =Recipe.objects.filter(recipe__name=recipe_title)
            if qs:      #if data found
           #convert the queryset values to pandas dataframe
              recipes_df=pd.DataFrame(qs.values())
              recipes_df['recipe_id']=recipes_df['recipe_id'].apply(get_recipename_from_id)
              recipes_df=recipes_df.to_html()

            print("Search Query:", recipe_title, "| Chart Type:", chart_type)

            print ('Exploring querysets:')
            print ('Case 1: Output of Recipe.objects.all()')
            qs=Recipe.objects.all()
            print (qs)

            print ('Case 2: Output of Recipe.objects.filter(book_name=book_title)')
            qs =Recipe.objects.filter(recipe__name=recipe_title)
            print (qs)

            print ('Case 3: Output of qs.values')
            print (qs.values())

            print ('Case 4: Output of qs.values_list()')
            print (qs.values_list())

            print ('Case 5: Output of Recipe.objects.get(id=1)')
            obj = Recipe.objects.get(id=1)
            print (obj)

        '''
       The following block is to get introduced to querysets
       #examples hidden to improve readability
       '''
     #pack up data to be sent to template in the context dictionary
    context = {
        'form': form,
        'recipe_title': recipe_title,
        'chart_type': chart_type,
        'recipes_df': recipes_df,
    }
    return render(request, 'recipes/records.html', context)

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipes:recipe_list')

    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                return redirect('recipes:recipe_list')
            else:
                error_message = "Invalid username or password."
        else:
            error_message = "Form is not valid."

    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})

# Logout View
def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')
