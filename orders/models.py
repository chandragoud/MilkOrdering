from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

class MilkOrder(models.Model):
    MORNING = 'morning'
    EVENING = 'evening'
    TIMESLOT_CHOICES = [
        (MORNING, 'Morning'),
        (EVENING, 'Evening'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    timeslot = models.CharField(max_length=10, choices=TIMESLOT_CHOICES)
    quantity = models.PositiveIntegerField()
    order_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timeslot} ({self.order_date})"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username


from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



