from django.urls import path
from .views import home, RecipeListView # type: ignore

app_name = "recipes"

urlpatterns = [
    path('', home, name='home'),
    path("list/", RecipeListView.as_view(), name="list"),
]
