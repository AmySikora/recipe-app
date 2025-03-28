from django import forms
from .models import Recipe

CHART_CHOICES = [
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
]

class RecipeSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=120,
        required=False,
        label="Search Recipes",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or ingredient...'
        })
    )

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'instructions', 'cooking_time', 'difficulty', 'pic', 'related_recipes']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
        }

    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        required=False,
        label="Chart Type"
    )
