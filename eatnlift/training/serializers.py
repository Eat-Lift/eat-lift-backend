from rest_framework import serializers
from .models import Exercise, ExerciseInWorkout, Workout, Workout, Muscles

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


