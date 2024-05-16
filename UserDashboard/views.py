from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request,'UserDashboard/index.html')

def projects_section_view(request,id):
    if id == "home":
        return render(request, 'UserDashboard/home.html')
    elif id == "grades":
        return render(request, 'UserDashboard/grades.html')
    elif id == "calendar":
        return render(request, 'UserDashboard/calendar.html')
    elif id == "settings":
        return render(request, 'UserDashboard/settings.html')
