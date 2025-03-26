from django import forms

CHART_CHOICES = (
    ('', 'Choose a chart type...'),
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
)

class RecipeSearchForm(forms.Form): 
    recipe_title = forms.CharField(
        max_length=120,
        required=False,
        label="Recipe Title",
        widget=forms.TextInput(attrs={'placeholder': 'Enter a recipe name...'})
    )
    recipe_ingredient = forms.CharField(
        max_length=120,
        required=False,
        label="Search by Ingredient",
        widget=forms.TextInput(attrs={'placeholder': 'Enter an ingredient...'})
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        label="Chart Type"
    )
