from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.db.models import Q, Avg
import pandas as pd

from .models import Recipe, Comment
from .forms import RecipeSearchForm, RecipeForm, CommentForm
from .utils import get_chart

# Homepage view
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Lists all recipes (requires login)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    login_url = '/login/'

# Displays details of a single recipe (requires login)
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'
    login_url = '/login/'

    # Add extra context to the detail page
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe = self.get_object()
        context['ingredients_list'] = recipe.ingredients.split(", ")
        context['instructions_list'] = recipe.instructions.split("\n")
        context['related_recipes'] = recipe.related_recipes.all()
        context['average_rating'] = recipe.comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
        context['comments'] = Comment.objects.filter(recipe=recipe).order_by('-created_at')
        context['is_hearted'] = recipe in self.request.user.saved_recipes.all()
        return context

    # Handle comment form submission
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_text = request.POST.get('comment')
        rating = request.POST.get('rating')

        if comment_text and rating:
            Comment.objects.create(
                recipe=self.object,
                user=request.user,
                text=comment_text,
                rating=int(rating)
            )

        # Handle heart/unheart submission
        heart_action = request.POST.get('heart_action')
        if heart_action == 'heart':
            request.user.saved_recipes.add(self.object)
        elif heart_action == 'unheart':
            request.user.saved_recipes.remove(self.object)

        return redirect('recipes:recipe_detail', pk=self.object.pk)

# User signup view
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

# About page
def about(request):
    return render(request, 'recipes/about.html')

# Displays charts based on recipe data (requires login)
@login_required(login_url='/login/')
def charts_view(request):
    chart = None
    chart_type = None
    labels = []
    data = []

    if request.method == 'POST':
        chart_type = request.POST.get('chart_type', '')
        qs = Recipe.objects.all()

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

        if chart_type:
            chart = get_chart(chart_type, df, labels=labels)

    return render(request, 'recipes/charts.html', {
        'chart': chart,
        'chart_type': chart_type
    })

# Search view with table and optional chart (requires login)
@login_required(login_url='/login/')
def search_view(request):
    form = RecipeSearchForm(request.GET or None)
    recipes_df = None
    recipes_df_raw = None
    chart = None
    chart_type = request.GET.get('chart_type', '#1') 
    search_term = request.GET.get('search_term', '')
    has_results = False

    qs = Recipe.objects.all()

    if search_term:
        qs = qs.filter(
            Q(name__icontains=search_term) |
            Q(ingredients__icontains=search_term)
        )

    if qs.exists():
        data = []
        labels = []

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
        recipes_df_raw = df
        chart = get_chart(chart_type, df, labels=labels)
        has_results = not df.empty

    form = RecipeSearchForm(initial={'search_term': '', 'chart_type': chart_type})

    context = {
        'form': form,
        'recipes_df': recipes_df,
        'recipes_df_raw': recipes_df_raw,
        'chart': chart,
        'has_results': has_results,
        'chart_type': chart_type,
    }

    return render(request, 'recipes/search.html', context)

# Add a new recipe
@login_required(login_url='/login/')
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

# Edit an existing recipe
@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.created_by != request.user:
        return HttpResponseForbidden("You are not allowed to edit this recipe.")

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recipe updated successfully!')
            return redirect('recipes:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'recipes/edit_recipe.html', {'form': form, 'recipe': recipe})

# Edit an existing comment
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe_detail', pk=comment.recipe.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'recipes/edit_comment.html', {'form': form, 'comment': comment})

# Delete a comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    recipe_id = comment.recipe.id
    comment.delete()
    messages.success(request, "Your comment was deleted.")
    return redirect('recipes:recipe_detail', pk=recipe_id)

# User login view
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

# User logout view
def logout_view(request):
    logout(request)
    return render(request, 'auth/success.html')
