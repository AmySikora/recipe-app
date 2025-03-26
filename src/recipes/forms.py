from django import forms

CHART_CHOICES = (
    ('', 'Choose a chart type...'),  # Default placeholder
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

class RecipeSearchForm(forms.Form): 
    recipe_title = forms.CharField(
        max_length=120,
        label="Recipe Title",
        widget=forms.TextInput(attrs={'placeholder': 'Enter a recipe name...'})
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        label="Chart Type"
    )
