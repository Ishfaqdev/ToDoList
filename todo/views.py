from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import SignUpForm, LoginForm, TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Task
from datetime import datetime, timedelta
from django.utils import timezone

# Create your views here.


def home(request):
    return render(request, 'todo/base.html')


@login_required(login_url='/login')
def all_tasks(request):
    all_tasks = Task.objects.filter(user=request.user)

    return render(request, 'todo/all-task.html', {'all_tasks': all_tasks})


@login_required(login_url='/login')
def add_task(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.created = timezone.now()
                if not task.due_date:
                    task.due_date = task.created + timezone.timedelta(days=7)
                task.save()
                return redirect('all-task')
        else:
            form = TaskForm()

        return render(request, 'todo/add-task.html', {'form': form})
    else:
        return HttpResponseRedirect('/login')


@login_required
def delete_task(request, task_id):
    if request.method == 'POST':
        task = Task.objects.get(id=task_id)
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('/all-task')


@login_required(login_url='/login')
def dashboard(request):
    all_tasks = Task.objects.filter(user=request.user)

    # Calculate statistics
    total_tasks = all_tasks.count()
    completed_tasks = all_tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }

    return render(request, 'todo/dashboard.html', context)


@login_required(login_url='/login')
def update_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        update = Task.objects.get(pk=id)
        form = TaskForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Your Task { task.title } has been updated Succesfully!')
            return redirect('all-task')
    else:
        update = Task.objects.get(pk=id)
        form = TaskForm(instance=update)

    return render(request, 'todo/update.html', {'form': form, 'task': task})


@login_required(login_url='/login')
def detail(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'todo/detail.html', {'task': task})


# User Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                user_name = form.cleaned_data['username']
                user_password = form.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    request.session['username'] = user_name
                    return redirect('all-task')
        else:
            form = LoginForm()

        return render(request, 'todo/login.html', {'form': form})
    else:
        return redirect('all-task')


# User Signup Form
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, 'Your account has been registered!! Now you can login')
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            request.session['username'] = form.cleaned_data['username']
            return redirect('all-task')
    else:
        form = SignUpForm()

    return render(request, 'todo/signup.html', {'form': form})


def about(request):
    return render(request, 'todo/about.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out!')
    return HttpResponseRedirect('/')
