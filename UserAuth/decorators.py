from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Teacher, Student
from django.shortcuts import render, redirect

def teacher_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'teacher'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('student:index')
    return _wrapped_view

def student_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'student'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('teachers:dashboard')
    return _wrapped_view
