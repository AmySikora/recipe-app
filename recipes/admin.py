from django.contrib import admin
from django.utils.html import format_html
from .models import Recipe
from django.utils.safestring import mark_safe

# Register your models here
# admin.site.register(Recipe)

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'show_related_recipes')  # Adds it to the list view
    readonly_fields = ('show_related_recipes',)      # Optional: adds it in the form

    def show_related_recipes(self, obj):
        related = obj.related_recipes.all()
        if not related:
            return "None"
        links = [
            f'<a href="/admin/recipes/recipe/{r.id}/change/">{r.name}</a>'
            for r in related
        ]
        return mark_safe(", ".join(links))

    show_related_recipes.short_description = "Related Recipes"

admin.site.register(Recipe, RecipeAdmin)