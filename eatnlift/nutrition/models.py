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