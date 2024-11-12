from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import FoodItem
from .serializers import FoodItemSerializer


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


@api_view(['DELETE'])
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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def foodItemSuggestions(request):
    query = request.query_params.get('name', None)

    if not query:
        return Response({"errors": ["No query parameter provided"]}, status=status.HTTP_400_BAD_REQUEST)

    matching_food_items = FoodItem.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True)

    return Response({"suggestions": list(matching_food_items)}, status=status.HTTP_200_OK)