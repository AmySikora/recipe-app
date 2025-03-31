from django.urls import path
from .views import (
    home,
    RecipeListView,
    RecipeDetailView,
    search_view,
    add_recipe,
    charts_view,
    about,
    edit_comment,
    delete_comment,
    edit_recipe
)

app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),  # Home page for the app

    path('recipes/', RecipeListView.as_view(), name='recipe_list'),  # View all recipes (login required)

    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),  # View details of a single recipe

    path('search/', search_view, name='search'),  # Search for recipes by name or ingredient, and show charts

    path('charts/', charts_view, name='charts'),  # Visual charts based on recipe data

    path('add/', add_recipe, name='add_recipe'),  # Add a new recipe (login required)

    path('about/', about, name='about'),  # Static About Me page

    path('comments/<int:pk>/edit/', edit_comment, name='edit_comment'),  # Edit a specific comment (login + ownership required)

    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),  # Delete a comment (login + ownership required)

    path('recipes/<int:pk>/edit/', edit_recipe, name='edit_recipe'),  # Edit a recipe (login + creator-only)
]
