from rest_framework import serializers
from .models import FoodItem, SavedFoodItem

class FoodItemSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.id')

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'calories', 'proteins', 'fats', 'carbohydrates', 'creator']


class SavedFoodItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    
    class Meta:
        model = SavedFoodItem
        fields = ['id', 'food_item', 'saved_at']