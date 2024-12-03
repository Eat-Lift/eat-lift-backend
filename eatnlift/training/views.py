from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Exercise, Workout, ExerciseInWorkout, Muscles, SavedExercise
from .serializers import ExerciseSerializer, WorkoutSerializer, ExerciseInWorkoutSerializer

# Exercises
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createExercise(request):
    data = request.data
    data['user'] = request.user.id
    serializer = ExerciseSerializer(data=data)

    if serializer.is_valid():
        if Exercise.objects.filter(name=serializer.validated_data['name'], user=request.user).exists():
            return Response(
                {"errors": ["Ja has creat un exercici amb aquest nom"]},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listExercises(request):
    exercises = Exercise.objects.filter(user=request.user)
    serializer = ExerciseSerializer(exercises, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editExercise(request, id):
    try:
        exercise = Exercise.objects.get(id=id, user=request.user)
    except Exercise.DoesNotExist:
        return Response({"errors": ["Aquest exercici no existeix"]}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ExerciseSerializer(exercise, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteExercise(request, id):
    try:
        exercise = Exercise.objects.get(id=id, user=request.user)
        exercise.delete()
        return Response({"success": "Exercici eliminat amb èxit"}, status=status.HTTP_204_NO_CONTENT)
    except Exercise.DoesNotExist:
        return Response({"errors": ["Aquest exercici no existeix"]}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveExercise(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except Exercise.DoesNotExist:
        return Response({"errors": ["L'exercici no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    saved_exercise, created = SavedExercise.objects.get_or_create(user=request.user, exercise=exercise)

    if created:
        return Response({"message": "Exercici desat correctament"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Ja has desat aquest exercici"}, status=status.HTTP_404_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unsaveExercise(request, exercise_id):
    try:
        saved_exercise = SavedExercise.objects.get(user=request.user, exercise_id=exercise_id)
    except SavedExercise.DoesNotExist:
        return Response({"errors": ["No has desat aquest exercici"]}, status=status.HTTP_404_NOT_FOUND)

    saved_exercise.delete()
    return Response({"message": "Exercici eliminat de la llista de desats"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def isExerciseSaved(request, exercise_id):
    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except Exercise.DoesNotExist:
        return Response({"errors": ["L'exercici no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    is_saved = SavedExercise.objects.filter(user=request.user, exercise=exercise).exists()
    return Response({"is_saved": is_saved}, status=status.HTTP_200_OK)


