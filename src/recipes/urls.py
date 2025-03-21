from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, records 

app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),
    path('list/', RecipeListView.as_view(), name='recipe_list'),
    path('list/<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipes/', records),
]
