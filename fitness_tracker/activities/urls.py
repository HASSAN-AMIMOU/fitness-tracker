# activities/urls.py
from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityRetrieveUpdateDestroyView,
    ActivityMetricsView,
    UserCreateView, UserDetailView
)

urlpatterns = [
    path('activities/', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    path('metrics/', ActivityMetricsView.as_view(), name='activity-metrics'),
]

# fitness_tracker/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('activities.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/register/', UserCreateView.as_view(), name='user-register'),
    path('users/me/', UserDetailView.as_view(), name='user-detail'),
    path('activities/history/', ActivityHistoryView.as_view(), name='activity-history'),
    path('activities/metrics/', ActivityMetricsView.as_view(), name='activity-metrics'),
]