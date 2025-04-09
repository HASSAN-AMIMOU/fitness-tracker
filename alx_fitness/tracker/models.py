from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings 
from django.core.validators import MinValueValidator



class Workout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.FloatField()
    
    def __str__(self):
        return f"{self.exercise} on {self.date}"
# Create your models here.
class User(models.Model):
    # Your custom user model implementation
    pass
class User(AbstractUser):
    # Add your custom fields here if needed
    
    class Meta:
        # Add this to avoid the clash
        swappable = 'AUTH_USER_MODEL'

    # Add related_name arguments to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='tracker_user_set',  # Changed from default
        related_query_name='tracker_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='tracker_user_set',  # Changed from default
        related_query_name='tracker_user',
    )

class Workout(models.Model):
    ACTIVITY_TYPES = [
        ('RUN', 'Running'),
        ('CYC', 'Cycling'),
        ('WL', 'Weightlifting'),
        ('SWIM', 'Swimming'),
        ('HIIT', 'HIIT'),
    ]
    
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=4, choices=ACTIVITY_TYPES)
    duration = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    distance = models.FloatField(null=True, blank=True)
    calories_burned = models.PositiveIntegerField()
    date = models.DateField()
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.get_activity_type_display()} on {self.date}"