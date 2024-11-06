from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random


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

class PasswordResetCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="password_reset_codes")
    code = models.CharField(max_length=6)
    expiration = models.DateTimeField()

    def save(self, *args, **kwargs):
        self.code = str(random.randint(100000, 999999))
        self.expiration = timezone.now() + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def is_valid(self):
        return timezone.now() < self.expiration