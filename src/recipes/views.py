from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RecipeSearchForm
import pandas as pd
from django.urls import reverse
from .utils import get_chart

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

# Home Page (Public)
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Records View with Search and Chart (Protected)
@login_required(login_url='/login/')
def records(request):
    form = RecipeSearchForm(request.POST or None)
    recipes_df = None
    chart = None
    qs = Recipe.objects.none()

    if request.method == 'POST':
        if form.is_valid():
            search_term = form.cleaned_data.get('search_term')
            chart_type = form.cleaned_data.get('chart_type')

            # If "Search" is clicked
            if 'search' in request.POST and search_term:
                qs = Recipe.objects.filter(
                    name__icontains=search_term
                ) | Recipe.objects.filter(
                    ingredients__icontains=search_term
                )

            # If "Show Recipes" is clicked
            elif 'show_recipes' in request.POST:
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
                        'Difficulty': recipe.difficulty
                    })
                    labels.append(recipe.name)

                recipes_df = pd.DataFrame(data)
                chart = get_chart(chart_type, recipes_df, labels=labels)
                recipes_df = recipes_df.to_html(escape=False)

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'chart': chart,
        'show_results': bool(recipes_df),
    }

    return render(request, 'recipes/records.html', context)


# Login View
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

# Logout View
def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')
