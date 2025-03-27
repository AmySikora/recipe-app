from django import forms

class RecipeSearchForm(forms.Form):
    search_term = forms.CharField(
        max_length=120,
        required=False,
        label="Search Recipes",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by name or ingredient...'
        })
    )

    chart_type = forms.CharField(
        max_length=10,
        required=False,
        widget=forms.HiddenInput()
    )
