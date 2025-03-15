from django.urls import path
from .views import home # type: ignore

urlpatterns = [
    path('', home, name='home'),
]
