from django import forms
from .models import Recipe, Comment

# Chart type options for displaying recipe data visually
CHART_CHOICES = [
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
]

# Form for searching recipes and selecting chart type
class RecipeSearchForm(forms.Form):
    # Optional search field for name or ingredients
    search_term = forms.CharField(
        max_length=120,
        required=False,
        label="Search Recipes",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or ingredient...'
        })
    )

    # Required field to choose the type of chart to display
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        required=True,
        label="Chart Type"
    )

# Form for creating or editing a recipe
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'instructions', 'cooking_time', 'pic']
        widgets = {
            'ingredients': forms.Textarea(attrs={
                'placeholder': 'e.g., 2 eggs, 1 cup flour, 1 tsp vanilla'
            }),
            'instructions': forms.Textarea(attrs={
                'placeholder': 'Step-by-step cooking instructions...'
            }),
            'cooking_time': forms.TextInput(attrs={
                'placeholder': 'e.g., 20 minutes'
            }),
        }
        help_texts = {
            'ingredients': 'Separate each ingredient with a comma or put each on a new line.',
            'instructions': 'Provide clear, step-by-step instructions for preparing the recipe.',
            'cooking_time': 'Enter a duration like "30 minutes" or "1 hour".',
        }

# Form for submitting a comment and rating on a recipe
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'text': 'Comment',
            'rating': 'Star Rating (1–5)',
        }
