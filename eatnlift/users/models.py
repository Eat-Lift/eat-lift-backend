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

class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    is_active = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None

    email = models.EmailField(blank=False, null=False, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    picture = models.URLField(max_length=255, blank=True)
    height = models.IntegerField(null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    goal = models.CharField(max_length = 15, choices=UserGoal.choices, null=True)
    activity = models.CharField(max_length = 22, choices=UserActivity.choices, null=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]