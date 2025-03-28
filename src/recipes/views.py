from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import RecipeSearchForm 
import pandas as pd
from django.urls import reverse
from .utils import get_chart
from .forms import RecipeForm
from django.contrib import messages

class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    login_url = '/login/'

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients_list'] = self.object.ingredients.split(", ")
        context['instructions_list'] = self.object.instructions.split("\n")
        context['related_recipes'] = self.object.related_recipes.all()
        return context

def home(request):
    return render(request, 'recipes/recipes_home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('recipes:recipe_list') 
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

@login_required(login_url='/login/')
def charts_view(request):
    qs = Recipe.objects.all()
    chart = None
    chart_type = '#1'  # default

    if request.method == 'POST':
        chart_type = request.POST.get('chart_type', '#1')

    if qs.exists():
        data = []
        labels = []

        for recipe in qs:
            labels.append(recipe.name)
            ingredient_count = len(recipe.ingredients.split(','))
            data.append({
                'Name': recipe.name,
                'Ingredients': recipe.ingredients,
                'Ingredient Count': ingredient_count,
                'Cooking Time (min)': recipe.cooking_time,
                'Difficulty': recipe.difficulty
            })

        df = pd.DataFrame(data)
        chart = get_chart(chart_type, df, labels=labels)

    return render(request, 'recipes/charts.html', {
        'chart': chart,
        'chart_type': chart_type
    })

def search_view(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    chart_type = None
    search_term = ''

    if request.method == 'POST' and form.is_valid():
        search_term = form.cleaned_data.get('search_term')
        chart_type = form.cleaned_data.get('chart_type')

    qs = Recipe.objects.all()

    if search_term:
        qs = qs.filter(name__icontains=search_term) | qs.filter(ingredients__icontains=search_term)

    if qs.exists():
        data = []
        labels = []
        
        # Reset form field after search is processed
        form = RecipeSearchForm(initial={'chart_type': chart_type})

        for recipe in qs:
            image_tag = f'<img src="{recipe.pic.url}" alt="{recipe.name}" height="60">'
            link = f'<a href="{reverse("recipes:recipe_detail", args=[recipe.id])}">{recipe.name}</a>'
            ingredient_count = len(recipe.ingredients.split(','))

            data.append({
                'Image': image_tag,
                'Name': link,
                'Ingredients': recipe.ingredients,
                'Number of Ingredients': ingredient_count,
                'Cooking Time (min)': recipe.cooking_time,
                'Difficulty': recipe.difficulty
            })

            labels.append(recipe.name)

        df = pd.DataFrame(data)
        recipes_df = df.to_html(escape=False)

        # Generates the chart:
        chart = get_chart(chart_type or '#1', df, labels=labels)

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart
    }

    return render(request, 'recipes/search.html', context)

def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.created_by = request.user
            recipe.save()
            form.save_m2m()
            messages.success(request, 'Recipe added successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipes:recipe_list')

    form = AuthenticationForm()
    error_message = None

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

    return render(request, 'auth/login.html', {
        'form': form,
        'error_message': error_message
    })

def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')
