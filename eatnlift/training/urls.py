from django.urls import path
from . import views

urlpatterns = [
    # Exercises
    path('exercises/', views.listExercises),
    path('exercises/saved', views.listSavedExercises),

    path('exercises/create', views.createExercise),
    path('exercises/bulkCreate', views.bulkCreateExercises),

    path('exercises/<int:id>', views.getExercise),
    path('exercises/<int:id>/edit', views.editExercise),
    path('exercises/<int:id>/delete', views.deleteExercise),

    path('exercises/<int:exercise_id>/save', views.saveExercise),
    path('exercises/<int:exercise_id>/unsave', views.unsaveExercise),
    path('exercises/<int:exercise_id>/isSaved', views.isExerciseSaved),

    path('exercises/<int:exercise_id>/weight', views.getLastSessionWeight),

    # Workouts
    path('workouts/', views.listWorkouts),
    
    path('workouts/create', views.createWorkout),
    path('workouts/bulkCreate', views.bulkCreateWorkouts),
    
    path('workouts/<int:id>', views.getWorkout),
    path('workouts/<int:id>/edit', views.editWorkout),
    path('workouts/<int:id>/delete', views.deleteWorkout),

    path('workouts/<int:id>/save', views.saveWorkout),
    path('workouts/<int:id>/unsave', views.unsaveWorkout),
    path('workouts/<int:id>/isSaved', views.isWorkoutSaved),

    # Routines
    path('routines/<int:user_id>', views.getRoutine),
    path('routines/<int:user_id>/edit', views.editRoutine),

    # Sessions
    path('sessions/<int:user_id>', views.getSession),
    path('sessions/<int:user_id>/edit', views.editSession),
    path('sessions/<int:user_id>/summary', views.getSessionsSummary),
]