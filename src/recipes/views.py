from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe  
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm  

# List View for Recipes (Protected)
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe
    template_name = 'recipes/recipes_list.html'
    login_url = '/login/'  # Redirect to login if not authenticated

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


# Home View (Public)
def home(request):
    return render(request, 'recipes/recipes_home.html')

# Protected Page (Requires Login)
@login_required(login_url='/login/')
def records(request):
    return render(request, 'recipes/records.html')

# Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('recipes:recipe_list')  # Redirect to recipes list if already logged in

    error_message = None
    form = AuthenticationForm()  # Create form object

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('recipes:recipe_list')  # Redirect to recipes list
            else:
                error_message = "Invalid username or password."
        else:
            error_message = "Form is not valid."

    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')  
