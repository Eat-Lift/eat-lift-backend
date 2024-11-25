from django.urls import path
from . import views

urlpatterns = [
    #   Food items
    path('foodItems/', views.listFoodItems),

    path('foodItems/create', views.createFoodItem),
    path('foodItems/bulkCreate', views.bulkCreateFoodItems),

    path('foodItems/<int:id>/edit', views.editFoodItem),
    path('foodItems/<int:id>/delete', views.deleteFoodItem),

    path('foodItems/<int:food_item_id>/save', views.saveFoodItem),
    path('foodItems/<int:food_item_id>/unsave', views.unsaveFoodItem),
    path('foodItems/<int:food_item_id>/isSaved', views.isFoodItemSaved),


    # Recipes
    path('recipes/', views.listRecipes),
    path('recipes/<int:id>', views.getRecipe),
    
    path('recipes/create', views.createRecipe),

    path('recipes/<int:id>/delete', views.deleteRecipe),
    path('recipes/<int:id>/edit', views.editRecipe),

    path('recipes/<int:recipe_id>/save', views.saveRecipe),
    path('recipes/<int:recipe_id>/unsave', views.unsaveRecipe),
    path('recipes/<int:recipe_id>/isSaved', views.isRecipeSaved),

    # Nutritional plans
    path('nutritionalPlans/<int:user_id>', views.getNutritionalPlan),
    path('nutritionalPlans/<int:user_id>/edit', views.editNutritionalPlan),

    # Meals
    path('meals/<int:user_id>', views.getMeals),
    path('meals/<int:user_id>/dates', views.getMealDates),
    path('meals/<int:user_id>/edit', views.editMeal),

]