from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Attendee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    event = models.ForeignKey(Event, related_name='attendees', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event = models.ForeignKey(Event, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Attendee, related_name='tasks', on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # Progress in percentage

    def __str__(self):
        return self.title