from django.contrib.auth.models import AbstractUser
from django.db import models


class UserActivity(models.TextChoices):
    SEDENTARY = 'Sedentarisme'
    LIGHT_ACTIVITY = 'Activitat lleugera'
    MODERATE_ACTIVITY = 'Activitat moderada'
    INTENSE_ACTIVITY = 'Activitat intensa'
    VERY_INTENSE_ACTIVITY = 'Activitat molt intensa'

class UserGoal(models.TextChoices):
    GAIN_MUSCLE = 'Guanyar múscul'
    LOSE_FAT = 'Perdre greix'
    MAINTAIN_WEIGHT = 'Mantenir el pes'

class UserGenre(models.TextChoices):
    MALE = 'Masculí'
    FEMALE = 'Femení'

class UserProfile(models.Model):
    birth_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length = 7, choices=UserGenre.choices, null=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    goal = models.CharField(max_length = 15, choices=UserGoal.choices, null=True)
    activity = models.CharField(max_length = 22, choices=UserActivity.choices, null=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    proteins = models.PositiveIntegerField(null=True, blank=True)
    fats = models.PositiveIntegerField(null=True, blank=True)
    carbohydrates = models.PositiveIntegerField(null=True, blank=True)

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None

    email = models.EmailField(blank=False, null=False, unique=True)
    description = models.TextField(null=True, blank=True)
    picture = models.URLField(default="gs://eatnlift-d2f8e.firebasestorage.app/uploads/user_profile/default_user.png", blank=True)
    profile_info = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
