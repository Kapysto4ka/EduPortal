from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import *
from .models import Teacher, Student
from django.contrib.auth import authenticate, login

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        user = authenticate(username=email,password=password)
        if user is not None:
            if user_type == 'teacher':
                print("TEACHER")
                try:
                    teacher = Teacher.objects.get(user=user)
                    login(request, user)
                    return redirect('teachers:dashboard')
                except Teacher.DoesNotExist:
                    pass
            elif user_type == 'student':
                print("STUDENT")
                try:
                    student = Student.objects.get(user=user)
                    login(request, user)
                    return redirect('students:index')
                except Student.DoesNotExist:
                    pass
        else:
            print("Error")

    return render(request, 'users/login.html')
