from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Muscles(models.TextChoices):
    PECTORAL = "Pectoral"
    DELTOIDES_ANTERIOR = "Deltoides anterior"
    DELTOIDES_POSTERIOR = "Deltoides posterior"
    DELTOIDES_MEDIAL = "Deltoides medial"
    BICEPS = "Biceps"
    TRICEPS = "Triceps"
    DORSAL = "Dorsal"
    ROMBOIDES = "Romboides"
    TRAPEZI = "Trapezi"
    LUMBAR = "Lumbar"
    QUADRICEPS = "Quadriceps"
    ISQUIOTIBIALS = "Isquiotibials"
    ADDUCTORS = "Adductors"
    GLUTI = "Gluti"
    PARAVERTEBRAL = "Paravertebral"
    ABDOMINALS = "Abdominals"

# Exercises

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.URLField(default="https://firebasestorage.googleapis.com/v0/b/eatnlift-d2f8e.firebasestorage.app/o/uploads%2Fexercises%2Fdefault_exercise.png?alt=media&token=22eed71d-9497-4e51-98af-ce46845b0615", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trained_muscles = models.JSONField(default=list, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="unique_exersice_per_user")
        ]

class SavedExercise(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="saved_by_users")

    class Meta:
        unique_together = ('user', 'exercise')
 
class Workout(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'user'], name="unique_workout_per_user")
        ]

class ExerciseInWorkout(models.Model):
    workout = models.ForeignKey('Workout', on_delete=models.CASCADE, related_name='exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

class SavedWorkout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_workouts")
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="saved_by_users")

    class Meta:
        unique_together = ('user', 'workout')

# Routines

class WeekDay(models.TextChoices):
    DILLUNS = 'DILLUNS'
    DIMARTS = 'DIMARTS'
    DIMECRES = 'DIMECRES'
    DIJOUS = 'DIJOUS'
    DIVENDRES = 'DIVENDRES'
    DISSABTE = 'DISSABTE'
    DIUMENGE = 'DIUMENGE'

class Routine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="routine")

class ExerciseInRoutine(models.Model):
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="exercises_in_routine")
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name="exercise_routines")
    week_day = models.CharField(max_length=20, choices=WeekDay.choices)

    class Meta:
        unique_together = ('routine', 'week_day', 'exercise')

# Sessions

class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sessions")
    date = models.DateField()

    class Meta:
        unique_together = ('user', 'date')

class SessionExercise(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)

class SessionSet(models.Model):
    session_exercise = models.ForeignKey(SessionExercise, on_delete=models.CASCADE, related_name="sets")
    weight = models.FloatField(validators=[MinValueValidator(0.1)])
    reps = models.PositiveIntegerField()