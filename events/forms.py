from django import forms
from .models import Event, Attendee, Task

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date']

class AttendeeForm(forms.ModelForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Attendee
        fields = ['name', 'email', 'event']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'event', 'assigned_to', 'progress']