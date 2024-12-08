from django.urls import path
from . import views

urlpatterns = [
    # Exercises
    path('exercises/', views.listExercises),

    path('exercises/create', views.createExercise),

    path('exercises/<int:id>', views.getExercise),
    path('exercises/<int:id>/edit', views.editExercise),
    path('exercises/<int:id>/delete', views.deleteExercise),

    path('exercises/<int:exercise_id>/save', views.saveExercise),
    path('exercises/<int:exercise_id>/unsave', views.unsaveExercise),
    path('exercises/<int:exercise_id>/isSaved', views.isExerciseSaved),

    # Workouts
    path('workouts/', views.listWorkouts),
    
    path('workouts/create', views.createWorkout),
    
    path('workouts/<int:id>', views.getWorkout),
    path('workouts/<int:id>/edit', views.editWorkout),
    path('workouts/<int:id>/delete', views.deleteWorkout),

    path('workouts/<int:id>/save', views.saveWorkout),
    path('workouts/<int:id>/unsave', views.unsaveWorkout),
    path('workouts/<int:id>/isSaved', views.isWorkoutSaved),
]