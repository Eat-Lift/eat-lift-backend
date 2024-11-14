from rest_framework import serializers
from .models import FoodItem, SavedFoodItem, Recipe, RecipeFoodItem

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

class RecipeFoodItemSerializer(serializers.ModelSerializer):
    food_item_name = serializers.ReadOnlyField(source='food_item.name')

    class Meta:
        model = RecipeFoodItem
        fields = ['id', 'food_item', 'food_item_name', 'grams']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_food_items = RecipeFoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'photo', 'creator', 'recipe_food_items']
        read_only_fields = ['creator']

