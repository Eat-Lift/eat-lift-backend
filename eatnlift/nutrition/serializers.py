from rest_framework import serializers
from .models import FoodItem, SavedFoodItem, Recipe, RecipeFoodItem, SavedRecipe, NutritionalPlan, RecipieNutritionalPlan, Meal, FoodItemMeal

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

class RecipeMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name']

class SavedRecipeSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = SavedRecipe
        fields = ['id', 'recipe']

class RecipieNutritionalPlanSerializer(serializers.ModelSerializer):
    recipe_name = serializers.CharField(source='recipe.name', read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), source='recipe')

    class Meta:
        model = RecipieNutritionalPlan
        fields = ['id', 'nutritional_plan', 'recipe_id', 'recipe_name', 'meal_type']


class NutritionalPlanSerializer(serializers.ModelSerializer):
    recipes = RecipieNutritionalPlanSerializer(
        many=True, source='nutritional_plan_recipes', read_only=True
    )

    class Meta:
        model = NutritionalPlan
        fields = ['id', 'user', 'recipes']

class CreateRecipieNutritionalPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipieNutritionalPlan
        fields = ['id', 'nutritional_plan', 'recipe', 'meal_type']

class FoodItemMealSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer()

    class Meta:
        model = FoodItemMeal
        fields = ['food_item', 'quantity']

class MealSerializer(serializers.ModelSerializer):
    food_items = FoodItemMealSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ['id', 'user', 'meal_type', 'date', 'food_items']


