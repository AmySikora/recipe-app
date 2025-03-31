from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Comment model allows users to rate and leave feedback on a recipe
class Comment(models.Model):
    # Link to the recipe this comment belongs to
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comments')
    # Link to the user who made the comment
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Text content of the comment
    text = models.TextField(max_length=500)
    # Rating from 1 to 5 stars
    rating = models.PositiveIntegerField(default=5)
    # Timestamp of when the comment was created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}⭐ on {self.recipe.name}"

# Main Recipe model
class Recipe(models.Model):
    # Recipe title
    name = models.CharField(max_length=255)
    # Optional description of the recipe
    description = models.TextField(blank=True, null=True)
    # Ingredients listed as a comma-separated string
    ingredients = models.TextField(help_text="List ingredients separated by commas")  
    # Estimated cooking time in minutes
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    # Image field for recipe photo (stored in 'recipes/' folder)
    pic = models.ImageField(upload_to='recipes/', default='recipes/no_picture.png')
    # Step-by-step instructions
    instructions = models.TextField(help_text="Step-by-step cooking instructions", default="No instructions provided.")
    # Optional related recipes (e.g., side dishes, complementary meals)
    related_recipes = models.ManyToManyField('self', blank=True)
    # User who created the recipe (can be null if deleted)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # Timestamp when recipe was created
    created_at = models.DateTimeField(auto_now_add=True)

    # Automatically calculate difficulty based on ingredients and cooking time
    @property
    def difficulty(self):
        ingredients = self.ingredients.split(", ")
        if self.cooking_time < 10 and len(ingredients) < 4:
            return "Easy"
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            return "Intermediate"
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            return "Hard"
        return "Unknown"

    def __str__(self):
        return str(self.name)

    # Returns the URL to view the recipe detail page
    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.pk})
