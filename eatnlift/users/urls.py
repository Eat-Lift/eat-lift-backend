from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signin', views.register),
    path('profile', views.profile),
]