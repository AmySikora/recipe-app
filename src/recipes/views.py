from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe  # Ensure Recipe is correctly imported
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
#to protect function-based views
from django.contrib.auth.decorators import login_required

# List View for Recipes (Protected)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'


# Detail View for a Single Recipe (Protected)
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'


# Home View (Public)
def home(request):
    return render(request, 'recipes/recipes_home.html')


# Protected function-based view for records
@login_required
def records(request):
    return render(request, 'recipes/records.html')


# Login View
def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:records')  # Redirect to a protected page
        else:
            error_message = 'Oops.. something went wrong'

    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout