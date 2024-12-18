from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Exercise, Workout, ExerciseInWorkout, Muscles, SavedExercise, SavedWorkout, Routine, ExerciseInRoutine, Session, SessionExercise, SessionSet
from .serializers import ExerciseSerializer, WorkoutSerializer, ExerciseInWorkoutSerializer, ExerciseInRoutineSerializer, SessionSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.db.models import Count

# Exercises
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createExercise(request):
    data = request.data
    data['user'] = request.user.id
    if 'picture' not in data or not data['picture']:
        data['picture'] = Exercise._meta.get_field('picture').default
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
    search_query = request.query_params.get('name', '')

    exercises = Exercise.objects.filter(
        user=request.user, name__icontains=search_query
    ).annotate(
        session_count=Count('sessionexercise')
    ).order_by('-session_count').values('id', 'name', 'session_count')

    return Response(list(exercises), status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getExercise(request, id):
    exercise = get_object_or_404(Exercise, id=id, user=request.user)
    serializer = ExerciseSerializer(exercise)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editExercise(request, id):
    try:
        exercise = Exercise.objects.get(id=id, user=request.user)
    except Exercise.DoesNotExist:
        return Response({"errors": ["Aquest exercici no existeix"]}, status=status.HTTP_404_NOT_FOUND)
    
    data = request.data.copy()
    
    if 'picture' not in data or not data['picture']:
        data['picture'] = exercise.picture

    serializer = ExerciseSerializer(exercise, data=data, partial=True)

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

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getLastSessionWeight(request, exercise_id):
    try:
        last_session_exercise = SessionExercise.objects.filter(
            exercise_id=exercise_id, session__user=request.user
        ).order_by('-session__date').first()

        if not last_session_exercise:
            return Response(
                {
                    "weight": 0,
                    "reps": 0,
                }, 
                status=status.HTTP_200_OK
            )

        first_set = SessionSet.objects.filter(
            session_exercise=last_session_exercise
        ).order_by('id').first()

        if not first_set:
            return Response(
                {
                    "weight": 0,
                    "reps": 0,
                }, 
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "weight": first_set.weight,
                "reps": first_set.reps,
            }, 
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            {"errors": [str(e)]}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# Workouts

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def createWorkout(request):
    data = request.data
    exercises_data = data.pop('exercises', [])
    user = request.user

    if Workout.objects.filter(name=data.get('name'), user=user).exists():
        return Response(
            {"errors": ["Ja has creat un entrenament amb aquest nom"]}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = WorkoutSerializer(data=data, context={'request': request})

    if serializer.is_valid():
        workout = serializer.save(user=user)

        for item in exercises_data:
            try:
                exercise = Exercise.objects.get(id=item)
                ExerciseInWorkout.objects.create(workout=workout, exercise=exercise)
            except Exercise.DoesNotExist:
                return Response(
                    {"errors": [f"Exercise with id {item} does not exist."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(WorkoutSerializer(workout).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editWorkout(request, id):
    exercises_data = request.data.pop('exercises', [])

    try:
        workout = Workout.objects.get(id=id, user=request.user)
    except Workout.DoesNotExist:
        return Response({"errors": ["Aquest entrenament no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkoutSerializer(workout, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

        ExerciseInWorkout.objects.filter(workout=workout).delete()

        for item in exercises_data:
            try:
                exercise = Exercise.objects.get(id=item)
                ExerciseInWorkout.objects.create(workout=workout, exercise=exercise)
            except Exercise.DoesNotExist:
                return Response(
                    {"errors": [f"Exercise with id {item} does not exist."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteWorkout(request, id):
    try:
        workout = Workout.objects.get(id=id, user=request.user)
        workout.delete()
        return Response({"success": "Entrenament eliminat amb èxit"}, status=status.HTTP_204_NO_CONTENT)
    except Workout.DoesNotExist:
        return Response({"errors": ["Aquest entrenament no existeix"]}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listWorkouts(request):
    search_query = request.query_params.get('name', '')
    workouts = Workout.objects.filter(user=request.user, name__icontains=search_query).values('id', 'name')
    return Response(list(workouts), status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getWorkout(request, id):
    try:
        workout = Workout.objects.get(id=id, user=request.user)
    except Workout.DoesNotExist:
        return Response({"errors": ["Entrenament no existeix o no tens accés"]}, status=status.HTTP_404_NOT_FOUND)

    serializer = WorkoutSerializer(workout)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def saveWorkout(request, id):
    try:
        workout = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"errors": ["L'entrenament no existeix"]}, status=status.HTTP_404_NOT_FOUND)

    saved_workout, created = SavedWorkout.objects.get_or_create(user=request.user, workout=workout)

    if created:
        return Response({"message": "Entrenament desat correctament"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"message": "Ja has desat aquest entrenament"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def unsaveWorkout(request, id):
    try:
        saved_workout = SavedWorkout.objects.get(user=request.user, workout_id=id)
    except SavedWorkout.DoesNotExist:
        return Response({"errors": ["No has desat aquest entrenament"]}, status=status.HTTP_400_BAD_REQUEST)

    saved_workout.delete()
    return Response({"message": "Entrenament eliminat de la llista de desats"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def isWorkoutSaved(request, id):
    try:
        workout = Workout.objects.get(id=id)
    except Workout.DoesNotExist:
        return Response({"errors": ["L'entrenament no existeix."]}, status=status.HTTP_404_NOT_FOUND)

    is_saved = SavedWorkout.objects.filter(user=request.user, workout=workout).exists()
    return Response({"is_saved": is_saved}, status=status.HTTP_200_OK)

# Routine
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editRoutine(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["No tens permís per editar aquest entrenament"]}, 
            status=status.HTTP_403_FORBIDDEN
        )

    routine, created = Routine.objects.get_or_create(user_id=user_id)

    exercises_data = request.data.get('exercises', [])

    ExerciseInRoutine.objects.filter(routine=routine).delete()

    if not exercises_data:
        return Response(
            {
                "message": "Entrenament actualitzat correctament. Tots els exercicis han estat eliminats.",
                "exercises": []
            }, 
            status=status.HTTP_200_OK
        )

    new_exercises = []
    week_day_counts = {}

    for exercise_data in exercises_data:
        try:
            exercise_id = exercise_data['id']
            week_day = exercise_data['week_day']

            if week_day not in week_day_counts:
                week_day_counts[week_day] = 0
            if week_day_counts[week_day] >= 15:
                return Response(
                    {"errors": [f"Només es permeten 15 exercicis per {week_day}."]}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            exercise = Exercise.objects.get(id=exercise_id)
            new_exercise = ExerciseInRoutine(
                routine=routine,
                exercise=exercise,
                week_day=week_day,
            )
            new_exercises.append(new_exercise)
            week_day_counts[week_day] += 1

        except Exercise.DoesNotExist:
            return Response(
                {"errors": [f"L'exercici amb ID {exercise_id} no existeix"]}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except KeyError as e:
            return Response(
                {"errors": [f"Falta el camp {str(e)} a l'exercici"]}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    ExerciseInRoutine.objects.bulk_create(new_exercises)

    updated_exercises = ExerciseInRoutine.objects.filter(routine=routine)
    serializer = ExerciseInRoutineSerializer(updated_exercises, many=True)

    return Response(
        {
            "message": "Entrenament actualitzat correctament",
            "exercises": serializer.data
        }, 
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getRoutine(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["No tens permís per veure aquest entrenament"]}, 
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        routine = Routine.objects.get(user_id=user_id)
        exercises = ExerciseInRoutine.objects.filter(routine=routine)
    except Routine.DoesNotExist:
        return Response(
            {
                "message": "Entrenament recuperat correctament",
                "exercises": []
            }, 
            status=status.HTTP_200_OK
        )

    serializer = ExerciseInRoutineSerializer(exercises, many=True)

    return Response(
        {
            "message": "Entrenament recuperat correctament",
            "exercises": serializer.data
        }, 
        status=status.HTTP_200_OK
    )

# Sessions

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSession(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    date = request.data.get('date')
    if not date:
        return Response({"errors": ["La data és un paràmetre obligatori"]},
                        status=status.HTTP_400_BAD_REQUEST)


    try:
        session = Session.objects.get(user_id=user_id, date=date)
    except Session.DoesNotExist:
        return Response({"user": user_id, "date": date, "exercises": []}, status=status.HTTP_200_OK)

    serializer = SessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editSession(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    data = request.data
    date = request.data.get('date')
    if not date:
        return Response({"errors": ["La data és un camp obligatori."]},
                        status=status.HTTP_400_BAD_REQUEST)

    session, created = Session.objects.get_or_create(user_id=user_id, date=date)

    SessionExercise.objects.filter(session=session).delete()

    exercises_data = data.get('exercises', [])
    for ex_data in exercises_data:
        exercise_id = ex_data.get('exercise')
        if exercise_id is None:
            return Response({"errors": ["Cada exercici ha de tenir el camp 'exercise'."]},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            exercise_obj = Exercise.objects.get(pk=exercise_id)
        except Exercise.DoesNotExist:
            return Response({"errors": [f"L'exercici amb ID {exercise_id} no existeix"]},
                            status=status.HTTP_404_NOT_FOUND)
        
        session_exercise = SessionExercise.objects.create(session=session, exercise=exercise_obj)

        sets_data = ex_data.get('sets', [])
        for s_data in sets_data:
            weight = s_data.get('weight')
            reps = s_data.get('reps')
            if weight is None or reps is None:
                return Response({"errors": ["Cada sèrie ha de tenir 'weight' i 'reps'."]},
                                status=status.HTTP_400_BAD_REQUEST)
            SessionSet.objects.create(session_exercise=session_exercise, weight=weight, reps=reps)

    serializer = SessionSerializer(session)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSessionsSummary(request, user_id):
    if request.user.id != user_id:
        return Response(
            {"errors": ["Aquest no és el teu usuari"]},
            status=status.HTTP_403_FORBIDDEN
        )

    request_date = request.data.get('date')
    if not request_date:
        return Response(
            {"errors": ["Data requerida"]},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        session_date = datetime.strptime(request_date, '%Y-%m-%d').date()
    except ValueError:
        return Response(
            {"errors": ["Data no vàlida"]},
            status=status.HTTP_400_BAD_REQUEST
        )

    catalan_weekdays = {
        'Monday': 'DILLUNS',
        'Tuesday': 'DIMARTS',
        'Wednesday': 'DIMECRES',
        'Thursday': 'DIJOUS',
        'Friday': 'DIVENDRES',
        'Saturday': 'DISSABTE',
        'Sunday': 'DIUMENGE'
    }

    week_day = catalan_weekdays[session_date.strftime('%A')]

    sessions_dates = list(Session.objects.filter(user_id=user_id).values_list('date', flat=True).order_by('date'))

    exercises_data = {}

    exercises_in_routine = ExerciseInRoutine.objects.filter(
        routine__user_id=user_id, week_day=week_day
    ).select_related('exercise')

    for exercise_in_routine in exercises_in_routine:
        exercise = exercise_in_routine.exercise

        if exercise.id not in exercises_data:
            exercises_data[exercise.id] = {
                "id": exercise.id,
                "name": exercise.name,
                "weights": []
            }

        sessions = Session.objects.filter(user_id=user_id).order_by('date')

        for session in sessions:
            first_set = SessionSet.objects.filter(
                session_exercise__session=session,
                session_exercise__exercise=exercise
            ).order_by('id').first()

            if first_set:
                exercises_data[exercise.id]["weights"].append(first_set.weight)

    return Response(
        {
            "sessions_dates": sessions_dates,
            "exercises": list(exercises_data.values())
        },
        status=status.HTTP_200_OK
    )
