from django.urls import path
from .views import WorkoutListCreate, WorkoutDetail

urlpatterns = [
    path('workouts/', WorkoutListCreate.as_view()),
    path('workouts/<int:pk>/', WorkoutDetail.as_view()),
]