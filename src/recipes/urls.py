from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, records, add_recipe


app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('records/', records, name='records'),
    path('recipes/add/', add_recipe, name='add_recipe'),
]
