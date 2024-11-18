from rest_framework import serializers
from .models import FoodItem, SavedFoodItem, Recipe, RecipeFoodItem, SavedRecipe

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
    name = serializers.ReadOnlyField(source='food_item.name')
    calories = serializers.ReadOnlyField(source='food_item.calories')
    proteins = serializers.ReadOnlyField(source='food_item.proteins')
    fats = serializers.ReadOnlyField(source='food_item.fats')
    carbohydrates = serializers.ReadOnlyField(source='food_item.carbohydrates')

    class Meta:
        model = RecipeFoodItem
        fields = ['id', 'food_item', 'name', 'quantity', 'calories', 'proteins', 'fats', 'carbohydrates']

class RecipeSerializer(serializers.ModelSerializer):
    recipe_food_items = RecipeFoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'picture', 'creator', 'recipe_food_items']
        read_only_fields = ['creator']

class SavedRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = SavedRecipe
        fields = ['id', 'recipe', 'saved_at']

