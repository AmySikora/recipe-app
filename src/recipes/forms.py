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

class ChartForm(forms.Form):
    chart_type = forms.ChoiceField(
        choices=[
            ('#1', 'Bar Chart (Cooking Time)'),
            ('#2', 'Pie Chart (Difficulty)'),
            ('#3', 'Line Chart (Ingredient Count)')
        ],
        label='Chart Type'
    )

