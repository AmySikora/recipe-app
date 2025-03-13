from django.db import models

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.TextField(help_text="List ingredients seperated by commas")
    cooking_time = models.PositiveIntegerField(help_text="Cooking time in minutes")
    difficulty = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name