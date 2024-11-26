from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('login/google', views.googleLogin),
    path('signin', views.signin),
    path('<int:id>', views.get),
    path('<int:id>/editPersonalInformation', views.editPersonalInformation),
    path('<int:id>/getPersonalInformation', views.getPersonalInformation),
    path('<int:id>/editProfile', views.editProfile),
    path('reset_password', views.resetPassword),
    path('new_password', views.newPassword),

        #Checks
    path('checks/<int:user_id>', views.getCheck),
    path('checks/<int:user_id>/dates', views.getCheckDates),
    path('checks/<int:user_id>/create', views.createCheck),
    path('checks/<int:user_id>/summary', views.getChecksSummary),
]