from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, search_view, add_recipe, charts_view, about, edit_comment, delete_comment, edit_recipe

app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),
    path('recipes/', RecipeListView.as_view(), name='recipe_list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('search/', search_view, name='search'),  
    path('charts/', charts_view, name='charts'),
    path('add/', add_recipe, name='add_recipe'),
    path('about/', about, name='about'),
    path('comments/<int:pk>/edit/', edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('recipes/<int:pk>/edit/', edit_recipe, name='edit_recipe'),
]
