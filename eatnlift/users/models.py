from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
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

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]