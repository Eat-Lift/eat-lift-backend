from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('login/google', views.googleLogin),
    path('signin', views.signin),
    path('<int:id>', views.get),
    path('<int:id>/editPersonalInformation', views.editPersonalInformation),
    path('<int:id>/editProfile', views.editProfile),
]