from django.urls import path
from . import views

urlpatterns = [
    #   Exercises
    path('exercises', views.listExercises),

    path('exercises/create', views.createExercise),

    path('exercises/<int:id>/edit', views.editExercise),
    path('exercises/<int:id>/delete', views.deleteExercise),

    path('exercises/<int:exercise_id>/save', views.saveExercise),
    path('exercises/<int:exercise_id>/unsave', views.unsaveExercise),
    path('exercises/<int:exercise_id>/isSaved', views.isExerciseSaved),
]