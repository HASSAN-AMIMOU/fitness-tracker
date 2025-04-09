from django.shortcuts import render
from rest_framework import generics
from .models import Workout
from .serializers import WorkoutSerializer

class WorkoutListCreate(generics.ListCreateAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

class WorkoutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
# Create your views here.


def home(request):
    return render(request, 'home.html')