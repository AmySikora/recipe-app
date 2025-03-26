from django import forms

CHART_CHOICES = (
    ('', 'Choose a chart type...'),
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart'),
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
        label="Chart Type"
    )
