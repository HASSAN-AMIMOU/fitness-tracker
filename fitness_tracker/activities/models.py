# activities/models.py
from django.db import models # type: ignore
from django.core.exceptions import ValidationError
from django.utils import timezone # type: ignore
from django.contrib.auth import get_user_model






User = get_user_model()

class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('RUN', 'Running'),
        ('SWIM', 'Swimming'),
        ('BIKE', 'Cycling'),
        ('GYM', 'Gym Workout'),
        ('WLK', 'Walking'),
        ('HIIT', 'HIIT'),
        ('YOGA', 'Yoga'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=4, choices=ACTIVITY_TYPES)
    duration = models.FloatField(help_text="Duration in minutes")
    distance = models.FloatField(
        help_text="Distance in kilometers", 
        null=True, 
        blank=True
    )
    calories_burned = models.PositiveIntegerField()
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    
    def clean(self):
        # Validate that required fields are present
        if not self.activity_type:
            raise ValidationError("Activity type is required")
        if not self.duration or self.duration <= 0:
            raise ValidationError("Duration must be a positive number")
        if not self.date:
            raise ValidationError("Date is required")
        
        # Validate distance for activities that should have it
        if self.activity_type in ['RUN', 'CYC', 'SWM', 'WALK'] and not self.distance:
            raise ValidationError(f"Distance is required for {self.get_activity_type_display()}")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs validation before saving
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username}'s {self.get_activity_type_display()} on {self.date.strftime('%Y-%m-%d')}"