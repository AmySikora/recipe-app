from django.urls import path
from .views import home, views, RecipeListView, RecipeDetailView, search_view, add_recipe, charts_view


app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('search/', search_view, name='search'),  
    path('charts/', charts_view, name='charts'),
    path('add/', add_recipe, name='add_recipe'),
    path('about/', views.about, name='about'),
]