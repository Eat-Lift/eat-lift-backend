from django.urls import path
from . import views

urlpatterns = [
    path('foodItems/', views.listFoodItems),

    path('foodItems/create', views.createFoodItem),
    path('foodItems/bulkCreate', views.bulkCreateFoodItems),

    path('foodItems/<int:id>/edit', views.editFoodItem),
    path('foodItems/<int:id>/delete', views.deleteFoodItem),

    path('food-items/<int:food_item_id>/save/', views.saveFoodItem),
    path('food-items/<int:food_item_id>/unsave/', views.unsaveFoodItem),
    path('foodItems/<int:food_item_id>/isSaved/', views.isFoodItemSaved),

    path('foodItems/suggestions/', views.foodItemSuggestions),
]