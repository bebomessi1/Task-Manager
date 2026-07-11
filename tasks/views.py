from django import forms
from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']


def home(request):
    tasks = Task.objects.all()

    pending_count = tasks.filter(status='pending').count()
    in_progress_count = tasks.filter(status='in_progress').count()
    done_count = tasks.filter(status='done').count()

    return render(request, 'tasks/home.html', {
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'done_count': done_count,
    })


def task_list(request):
    selected_status = request.GET.get('status', '')
    tasks = Task.objects.all().order_by('-created_at')

    if selected_status:
        tasks = tasks.filter(status=selected_status)

    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'selected_status': selected_status,
    })


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Create Task',
    })


def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render(request, 'tasks/task_detail.html', {'task': task})


def update_task(request, id):
    task = get_object_or_404(Task, id=id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task',
    })