from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import FoodItem, SavedFoodItem, Recipe, RecipeFoodItem, SavedRecipe
from .serializers import FoodItemSerializer, RecipeSerializer, RecipeFoodItemSerializer, RecipeMinimalSerializer


# FoodItems section

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createFoodItem(request):
    data = request.data
    data['creator'] = request.user.id
    serializer = FoodItemSerializer(data=data)

    if serializer.is_valid():
        if FoodItem.objects.filter(name=serializer.validated_data['name'], creator=request.user).exists():
            return Response({"errors": ["Ja has creat un aliment amb aquest nom"]}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(creator=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editFoodItem(request, id):
    try:
        food_item = FoodItem.objects.get(id=id, creator=request.user)
    except FoodItem.DoesNotExist:
        return Response({"errors": ["Aquest aliment no existeix"]}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = FoodItemSerializer(food_item, data=request.data, partial=True)
    
    if serializer.is_valid():
        if FoodItem.objects.filter(name=serializer.validated_data['name'], creator=request.user).exists():
            return Response({"errors": ["Ja has creat un aliment amb aquest nom"]}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteFoodItem(request, id):
    try:
        food_item = FoodItem.objects.get(id=id, creator=request.user)
        food_item.delete()
        return Response({"success": "Aliment eliminat amb èxit"}, status=status.HTTP_204_NO_CONTENT)
    except FoodItem.DoesNotExist:
        return Response({"errors": ["Aquest aliment no existeix"]}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listFoodItems(request):
    search_query = request.query_params.get('name', None)

    if search_query:
        food_items = FoodItem.objects.filter(name__icontains=search_query)
    else:
        food_items = FoodItem.objects.all()

    serializer = FoodItemSerializer(food_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bulkCreateFoodItems(request):
    food_items_data = request.data.get('food_items', [])
    
    if not isinstance(food_items_data, list):
        return Response({"errors": ["Expected a list of food items."]}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = FoodItemSerializer(data=food_items_data, many=True)
    
    if serializer.is_valid():
        food_items = [
            FoodItem(
                name=item['name'],
                calories=item['calories'],
                proteins=item['proteins'],
                fats=item['fats'],
                carbohydrates=item['carbohydrates'],
                creator=request.user
            ) for item in serializer.validated_data
        ]
        
        FoodItem.objects.bulk_create(food_items)
        return Response({"message": "Food items created successfully."}, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveFoodItem(request, food_item_id):
    try:
        food_item = FoodItem.objects.get(id=food_item_id)
    except FoodItem.DoesNotExist:
        return Response({"errors": ["L'aliment no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    saved_food, created = SavedFoodItem.objects.get_or_create(user=request.user, food_item=food_item)

    if created:
        return Response({"message": "Aliment desat correctament"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Ja has desat aquest aliment"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unsaveFoodItem(request, food_item_id):
    try:
        saved_food = SavedFoodItem.objects.get(user=request.user, food_item_id=food_item_id)
    except SavedFoodItem.DoesNotExist:
        return Response({"errors": ["No has desat aquest aliment"]}, status=status.HTTP_404_NOT_FOUND)

    saved_food.delete()
    return Response({"message": "Aliment eliminat de la llista de desats"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def isFoodItemSaved(request, food_item_id):
    try:
        food_item = FoodItem.objects.get(id=food_item_id)
    except FoodItem.DoesNotExist:
        return Response({"errors": ["Food item does not exist."]}, status=status.HTTP_404_NOT_FOUND)

    is_saved = SavedFoodItem.objects.filter(user=request.user, food_item=food_item).exists()
    return Response({"is_saved": is_saved}, status=status.HTTP_200_OK)



# Recipes section

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createRecipe(request):
    data = request.data
    food_items_data = data.pop('food_items', [])
    creator = request.user

    if Recipe.objects.filter(name=data.get('name'), creator=creator).exists():
        return Response(
            {"errors": ["Ja has creat una recepta amb aquest nom"]}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if 'picture' not in data or not data['picture']:
        data['picture'] = Recipe._meta.get_field('picture').default

    serializer = RecipeSerializer(data=data, context={'request': request})

    if serializer.is_valid():
        recipe = serializer.save(creator=creator)

        for item in food_items_data:
            food_item_id = item.get('food_item')
            quantity = item.get('quantity')
            try:
                food_item = FoodItem.objects.get(id=food_item_id)
                RecipeFoodItem.objects.create(recipe=recipe, food_item=food_item, quantity=quantity)
            except FoodItem.DoesNotExist:
                return Response(
                    {"errors": [f"Food item with id {food_item_id} does not exist."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(RecipeSerializer(recipe).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editRecipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id, creator=request.user)
    except Recipe.DoesNotExist:
        return Response({"errors": ["Aquesta recepta no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    recipe_food_items_data = request.data.pop('food_items', [])
    
    serializer = RecipeSerializer(recipe, data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if Recipe.objects.filter(name=serializer.validated_data['name'], creator=request.user).exists():
            return Response({"errors": ["Ja has creat una recepta amb aquest nom"]}, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()

    RecipeFoodItem.objects.filter(recipe=recipe).delete()
    for item_data in recipe_food_items_data:
        try:
            food_item = FoodItem.objects.get(id=item_data['food_item'])
        except FoodItem.DoesNotExist:
            return Response({"errors": [f"Food item with id {item_data['food_item']} does not exist"]},
                            status=status.HTTP_400_BAD_REQUEST)
        RecipeFoodItem.objects.create(
            recipe=recipe,
            food_item=food_item,
            quantity=item_data.get('quantity', 0)
        )

    # Return the updated recipe data
    return Response(RecipeSerializer(recipe).data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteRecipe(request, id):
    try:
        recipe = Recipe.objects.get(id=id, creator=request.user)
        recipe.delete()
        return Response({"success": "Recepta eliminada amb èxit"}, status=status.HTTP_204_NO_CONTENT)
    except Recipe.DoesNotExist:
        return Response({"errors": ["Aquesta recepta no existeix"]}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listRecipes(request):
    search_query = request.query_params.get('name', None)

    if search_query:
        recipes = Recipe.objects.filter(name__icontains=search_query, creator=request.user)
    else:
        recipes = Recipe.objects.filter(creator=request.user)

    serializer = RecipeMinimalSerializer(recipes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRecipe(request, id):
    try:
        # Retrieve the recipe by ID
        recipe = Recipe.objects.get(id=id)
    except Recipe.DoesNotExist:
        return Response({"errors": ["Recipe does not exist or you do not have access"]}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the recipe including related food items
    serializer = RecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveRecipe(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return Response({"errors": ["La recepta no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    saved_recipe, created = SavedRecipe.objects.get_or_create(user=request.user, recipe=recipe)

    if created:
        return Response({"message": "Recepta desada correctament"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Ja has desat aquesta recepta"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unsaveRecipe(request, recipe_id):
    try:
        saved_recipe = SavedRecipe.objects.get(user=request.user, recipe_id=recipe_id)
    except SavedRecipe.DoesNotExist:
        return Response({"errors": ["No has desat aquesta recepta"]}, status=status.HTTP_404_NOT_FOUND)

    saved_recipe.delete()
    return Response({"message": "Recepta eliminada de la llista de desats"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def isRecipeSaved(request, recipe_id):
    try:
        recipe = Recipe.objects.get(id=recipe_id)
    except RecipeItem.DoesNotExist:
        return Response({"errors": ["Recipe item does not exist."]}, status=status.HTTP_404_NOT_FOUND)

    is_saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    return Response({"is_saved": is_saved}, status=status.HTTP_200_OK)
