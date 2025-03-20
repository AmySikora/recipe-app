from django.db import models
from django.shortcuts import reverse
from django.urls import reverse

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(help_text="List ingredients seperated by commas")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True, null=True)
    pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')

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