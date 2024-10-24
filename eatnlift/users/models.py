from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    first_name = None
    last_name = None
    is_active = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]