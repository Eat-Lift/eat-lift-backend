from django.db import models
from django.conf import settings

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


class Exercise(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    picture = models.URLField(default="https://firebasestorage.googleapis.com/v0/b/eatnlift-d2f8e.firebasestorage.app/o/uploads%2Frecipes%2Frecipe-default-image.png?alt=media&token=d8274913-c9a8-47a8-b4c5-9791190e774f", blank=True)
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