from django import forms
from .models import Recipe, Comment

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

    chart_type = forms.ChoiceField(
            choices=CHART_CHOICES,
            required=True,
            label="Chart Type"
        )
    
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'description', 'ingredients', 'instructions', 'cooking_time', 'pic']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 4}),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
        }

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
    
