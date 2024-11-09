from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description', 'picture']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'genre', 'height', 'weight', 'goal', 'activity', 'calories', 'proteins', 'fats', 'carbohydrates']