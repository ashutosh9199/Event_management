from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Event, Attendee, Task
from .forms import EventForm, AttendeeForm, TaskForm

def home(request):
    return render(request, 'events/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('events')
        else:
            return render(request, 'events/login.html', {'error': 'Invalid credentials'})
    return render(request, 'events/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                return redirect('login')
            except:
                return render(request, 'events/register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'events/register.html', {'error': 'Passwords do not match'})
    return render(request, 'events/register.html')

@login_required
def events_page(request):
    events = Event.objects.filter(created_by=request.user)
    return render(request, 'events/events.html', {'events': events})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('events')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        event.delete()
        return redirect('events')
    return render(request, 'events/event_confirm_delete.html', {'event': event})

@login_required
def attendee_create(request, event_id):
    event = get_object_or_404(Event, pk=event_id, created_by=request.user)
    if request.method == 'POST':
        form = AttendeeForm(request.POST)
        if form.is_valid():
            attendee = form.save(commit=False)
            attendee.event = event
            attendee.save()
            task_id = form.cleaned_data.get('task_id')
            if task_id:
                task = get_object_or_404(Task, pk=task_id, event=event)
                task.assigned_to = attendee
                task.save()
            return redirect('event_detail', pk=event_id)
    else:
        form = AttendeeForm()
    return render(request, 'events/attendee_form.html', {'form': form, 'event': event})

@login_required
def task_create(request, event_id):
    event = get_object_or_404(Event, pk=event_id, created_by=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.event = event
            task.save()
            return redirect('event_detail', pk=event_id)
    else:
        form = TaskForm()
    return render(request, 'events/task_form.html', {'form': form, 'event': event})

@login_required
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    attendees = event.attendees.all()
    tasks = event.tasks.all()
    return render(request, 'events/event_detail.html', {'event': event, 'attendees': attendees, 'tasks': tasks})