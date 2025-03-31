from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Recipe

# Custom admin interface for the Recipe model
class RecipeAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin
    list_display = ('name', 'show_related_recipes')

    # Make this field read-only in the form view
    readonly_fields = ('show_related_recipes',)

    # Custom method to show links to related recipes in the admin panel
    def show_related_recipes(self, obj):
        related = obj.related_recipes.all()  # Get all related recipes
        if not related:
            return "None"
        # Create admin links for each related recipe
        links = [
            f'<a href="/admin/recipes/recipe/{r.id}/change/">{r.name}</a>'
            for r in related
        ]
        return mark_safe(", ".join(links))  # Safely render HTML

    # Set column name in admin list view
    show_related_recipes.short_description = "Related Recipes"

# Register the Recipe model with the customized admin interface
admin.site.register(Recipe, RecipeAdmin)
