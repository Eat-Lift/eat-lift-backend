from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    is_active = None
    is_staff = None
    is_superuser = None
    date_joined = None
    last_login = None
    groups = None
    user_permissions = None

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]