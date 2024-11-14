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

    path('foodItems/suggestions/', views.foodItemSuggestions),


    # Recipes
    path('recipes/', views.listRecipes),
    
    path('recipes/create', views.createRecipe),


]