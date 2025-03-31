from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User

# Let users add comments and rating to recipes
class Comment(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    rating = models.PositiveIntegerField(default=5)  # Allow 1–5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}⭐ on {self.recipe.name}"

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(help_text="List ingredients separated by commas")  
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True, null=True) 
    pic = models.ImageField(upload_to='recipes/', default='recipes/no_picture.png')
    instructions = models.TextField(help_text="Step-by-step cooking instructions", default="No instructions provided.")
    related_recipes = models.ManyToManyField('self', blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
  
    # determine recipe difficulty
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

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.pk})
