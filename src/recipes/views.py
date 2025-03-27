from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RecipeSearchForm
from .forms import ChartForm 
import pandas as pd
from django.urls import reverse
from .utils import get_chart

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
        return context

def home(request):
    return render(request, 'recipes/recipes_home.html')

@login_required(login_url='/login/')
def records(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    all_recipes_df = None
    all_chart = None
    show_all = False

    if request.method == 'POST':
        if 'search' in request.POST and form.is_valid():
            search_term = form.cleaned_data.get('search_term')
            chart_type = form.cleaned_data.get('chart_type')

            qs = Recipe.objects.filter(
                name__icontains=search_term
            ) | Recipe.objects.filter(
                ingredients__icontains=search_term
            )

            if search_term and qs.exists():
                data = []
                labels = []

                for recipe in qs:
                    link = f'<a href="{reverse("recipes:recipe_detail", args=[recipe.id])}">{recipe.name}</a>'
                    data.append({
                        'Name': link,
                        'Ingredients': recipe.ingredients,
                        'Cooking Time (min)': recipe.cooking_time,
                        'Difficulty': recipe.difficulty,
                        'Ingredient Count': len(recipe.ingredients.split(','))
                    })
                    labels.append(recipe.name)

                df = pd.DataFrame(data)
                recipes_df = df.to_html(escape=False)
                chart = get_chart(chart_type, df, labels=labels)

            form = RecipeSearchForm()  # Reset form

        elif 'show_all' in request.POST:
            show_all = True
            qs = Recipe.objects.all()

            if qs.exists():
                data = []
                labels = []

                for recipe in qs:
                    link = f'<a href="{reverse("recipes:recipe_detail", args=[recipe.id])}">{recipe.name}</a>'
                    data.append({
                        'Name': link,
                        'Ingredients': recipe.ingredients,
                        'Cooking Time (min)': recipe.cooking_time,
                        'Difficulty': recipe.difficulty,
                        'Ingredient Count': len(recipe.ingredients.split(','))
                    })
                    labels.append(recipe.name)

                df = pd.DataFrame(data)
                all_recipes_df = df.to_html(escape=False)
                all_chart = get_chart('#1', df, labels=labels)  # default bar chart for all

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
        'all_recipes_df': all_recipes_df,
        'all_chart': all_chart,
        'show_all': show_all,
    }

    return render(request, 'recipes/records.html', context)
   
def charts_view(request):
    form = ChartForm(request.POST or None)
    chart = None

    if request.method == 'POST' and form.is_valid():
        chart_type = form.cleaned_data['chart_type']
        qs = Recipe.objects.all()  # All recipes, no filtering

        if qs.exists():
            data = []
            labels = []

            for recipe in qs:
                labels.append(recipe.name)
                data.append({
                    'Name': recipe.name,
                    'Ingredients': recipe.ingredients,
                    'Cooking Time (min)': recipe.cooking_time,
                    'Difficulty': recipe.difficulty,
                    'Ingredient Count': len(recipe.ingredients.split(','))
                })

            df = pd.DataFrame(data)
            chart = get_chart(chart_type, df, labels=labels)

    return render(request, 'recipes/charts.html', {
        'form': form,
        'chart': chart
    })

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
