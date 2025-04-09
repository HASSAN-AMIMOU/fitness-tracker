from django.urls import path
from .views import WorkoutListCreate, WorkoutDetail,  UserCreateView, ActivityListCreateView, ActivityDetailView, ActivityMetricsView

urlpatterns = [
    path('workouts/', WorkoutListCreate.as_view()),
    path('workouts/<int:pk>/', WorkoutDetail.as_view()),
     path('users/register/', UserCreateView.as_view(), name='user-register'),
    path('activities/', ActivityListCreateView.as_view(), name='activity-list'),
    path('activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('activities/metrics/', ActivityMetricsView.as_view(), name='activity-metrics'),
]