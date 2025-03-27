from django import forms

CHART_CHOICES = (
    ('', 'Choose a chart type...'),
    ('#1', 'Bar chart (Time + Ingredients)'),
    ('#2', 'Pie chart (Difficulty Levels)'),
    ('#3', 'Line chart (Cooking Time)'),
)

class RecipeSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=120,
        required=False,
        label="Search Recipes",
        widget=forms.TextInput(attrs={'placeholder': 'Search by name or ingredient...'})
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        label="Chart Type",
        required=False
    )
