from django import forms

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
        required=False,
        label="Chart Type"
    )
