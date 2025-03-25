from django import forms  # Import Django forms

# Define chart choices as a tuple of tuples
CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

# Define class-based Form
class RecipeSearchForm(forms.Form): 
    recipe_title = forms.CharField(max_length=120, label="Recipe Title")
    chart_type = forms.ChoiceField(choices=CHART_CHOICES, label="Chart Type")
