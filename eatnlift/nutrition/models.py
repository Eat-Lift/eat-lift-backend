from django.db import models
from django.conf import settings

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    calories = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    carbohydrates = models.FloatField()
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_items')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'creator'], name='unique_name_per_creator')
        ]

    def __str__(self):
        return self.name


class SavedFoodItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_food_items")
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name="saved_by_users")
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'food_item')


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.URLField(default="https://firebasestorage.googleapis.com/v0/b/eatnlift-d2f8e.firebasestorage.app/o/uploads%2Frecipes%2Frecipe-default-image.png?alt=media&token=d8274913-c9a8-47a8-b4c5-9791190e774f", blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food_items = models.ManyToManyField('FoodItem', through='RecipeFoodItem', related_name='recipes')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'creator'], name='unique_recipe_per_creator')
        ]

    def __str__(self):
        return self.name


class RecipeFoodItem(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_food_items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, related_name='recipe_food_items')
    quantity = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'food_item'], name='unique_food_in_recipe')
        ]

    def __str__(self):
        return f"{self.food_item.name} in {self.recipe.name} ({self.quantity}g)"

class SavedRecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_recipes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="saved_by_users")

    class Meta:
        unique_together = ('user', 'recipe')

class Meal(models.TextChoices):
    BREAKFAST = 'ESMORZAR'
    LUNCH = 'DINAR'
    SNACK = 'BERENAR'
    DINNER = 'SOPAR'

class NutritionalPlan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="nutritional_plan")

class RecipieNutritionalPlan(models.Model):
    nutritional_plan = models.ForeignKey(NutritionalPlan, on_delete=models.CASCADE, related_name="nutritional_plan_recipes")
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name="meal_recipes")
    meal_type = models.CharField(max_length=20, choices=Meal.choices)

    class Meta:
        unique_together = ('nutritional_plan', 'meal_type', 'recipe')