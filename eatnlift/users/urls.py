from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('signin', views.signin),
    path('<int:id>', views.get),
    path('<int:id>/edit', views.edit),
]