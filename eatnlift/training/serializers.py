from rest_framework import serializers
from .models import Exercise, ExerciseInWorkout, Workout, Workout, Muscles, Routine, ExerciseInRoutine, Session, SessionExercise, SessionSet

class ExerciseSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    trained_muscles = serializers.ListField(
        child=serializers.ChoiceField(choices=Muscles.choices),
        required=True
    )

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'picture', 'user', 'trained_muscles']

class ExerciseInWorkoutSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = ExerciseInWorkout
        fields = ['exercise', 'workout']

class WorkoutSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    exercises = ExerciseInWorkoutSerializer(many=True, read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'user', 'exercises']

class ExerciseInRoutineSerializer(serializers.ModelSerializer):
    exercise = ExerciseSerializer()

    class Meta:
        model = ExerciseInRoutine
        fields = ['week_day', 'exercise']



class RoutineSerializer(serializers.ModelSerializer):
    exercises = ExerciseInRoutineSerializer(
        many=True, 
        source='exercises_in_routine', 
        read_only=True
    )

    class Meta:
        model = Routine
        fields = ['user', 'exercises']

class SessionSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionSet
        fields = ['weight', 'reps']

class BriefExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name']

class SessionExerciseSerializer(serializers.ModelSerializer):
    sets = SessionSetSerializer(many=True, read_only=True)
    exercise = BriefExerciseSerializer(read_only=True)

    class Meta:
        model = SessionExercise
        fields = ['exercise', 'sets']

class SessionSerializer(serializers.ModelSerializer):
    exercises = SessionExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['user', 'date', 'exercises']

