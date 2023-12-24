from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, choices=[(
        'Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')

    def __str__(self):
        return self.title
