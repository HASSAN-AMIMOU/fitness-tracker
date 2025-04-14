# activities/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from datetime import datetime
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from collections import defaultdict

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Activity.objects.all()
    
    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if obj.user != request.user:
            raise PermissionDenied("You don't have permission to access this activity.")

class ActivityHistoryView(generics.ListAPIView):
    serializer_class = ActivityHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activity_type']
    search_fields = ['notes']
    ordering_fields = ['date', 'duration', 'calories_burned']
    ordering = ['-date']  # Default ordering

    def get_queryset(self):
        queryset = Activity.objects.filter(user=self.request.user)
        
        # Date range filtering
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            try:
                start_date = parse_date(start_date)
                if start_date:
                    queryset = queryset.filter(date__date__gte=start_date)
            except ValueError:
                pass
        
        if end_date:
            try:
                end_date = parse_date(end_date)
                if end_date:
                    queryset = queryset.filter(date__date__lte=end_date)
            except ValueError:
                pass
        
        # Activity type filtering (handled automatically by filterset_fields)
        
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add summary information to the response
        queryset = self.filter_queryset(self.get_queryset())
        
        response.data['summary'] = {
            'total_activities': queryset.count(),
            'total_duration': queryset.aggregate(total=Sum('duration'))['total'] or 0,
            'total_calories': queryset.aggregate(total=Sum('calories_burned'))['total'] or 0,
            'total_distance': queryset.aggregate(total=Sum('distance'))['total'] or 0,
        }
        
        return response



class ActivityMetricsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        # Get base queryset filtered by user
        user_activities = Activity.objects.filter(user=request.user)
        
        # Calculate time periods
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)
        
        # Main metrics calculation
        metrics = {
            'lifetime': self._calculate_metrics(user_activities),
            'yearly': self._calculate_metrics(user_activities.filter(date__gte=year_ago)),
            'monthly': self._calculate_metrics(user_activities.filter(date__gte=month_ago)),
            'weekly': self._calculate_metrics(user_activities.filter(date__gte=week_ago)),
            'daily': self._calculate_metrics(user_activities.filter(date__date=today)),
            'trends': self._calculate_trends(user_activities),
            'activity_distribution': self._activity_distribution(user_activities),
        }
        
        return Response(metrics)
    
    def _calculate_metrics(self, queryset):
        aggregates = queryset.aggregate(
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_calories=Sum('calories_burned'),
            count=Count('id')
        )
        
        return {
            'activity_count': aggregates['count'] or 0,
            'total_duration_minutes': aggregates['total_duration'] or 0,
            'total_duration_hours': round((aggregates['total_duration'] or 0) / 60, 1),
            'total_distance_km': aggregates['total_distance'] or 0,
            'total_calories': aggregates['total_calories'] or 0,
            'avg_duration': round((aggregates['total_duration'] or 0) / max(1, aggregates['count'] or 1), 1),
            'avg_calories_per_activity': round((aggregates['total_calories'] or 0) / max(1, aggregates['count'] or 1)),
        }
    
    def _calculate_trends(self, queryset):
        # Weekly trends
        weekly_data = (
            queryset
            .annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(
                duration=Sum('duration'),
                distance=Sum('distance'),
                calories=Sum('calories_burned'),
                count=Count('id')
            )
            .order_by('week')
        )
        
        # Monthly trends
        monthly_data = (
            queryset
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(
                duration=Sum('duration'),
                distance=Sum('distance'),
                calories=Sum('calories_burned'),
                count=Count('id')
            )
            .order_by('month')
        )
        
        # Activity type trends
        activity_trends = defaultdict(list)
        activity_types = queryset.values_list('activity_type', flat=True).distinct()
        
        for activity_type in activity_types:
            type_data = (
                queryset
                .filter(activity_type=activity_type)
                .annotate(month=TruncMonth('date'))
                .values('month')
                .annotate(
                    duration=Sum('duration'),
                    distance=Sum('distance'),
                    calories=Sum('calories_burned'),
                    count=Count('id')
                )
                .order_by('month')
            )
            activity_trends[activity_type] = list(type_data)
        
        return {
            'weekly': list(weekly_data),
            'monthly': list(monthly_data),
            'by_activity_type': dict(activity_trends),
        }
    
    def _activity_distribution(self, queryset):
        return list(
            queryset
            .values('activity_type')
            .annotate(
                count=Count('id'),
                total_duration=Sum('duration'),
                total_calories=Sum('calories_burned'),
                avg_duration=Avg('duration'),
                avg_calories=Avg('calories_burned')
            )
            .order_by('-count')
        )