from django import forms
from UserAuth.models import *

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'group']
        labels = {
            'name': 'Назва предмета',
            'description': 'Опис предмета', 
            'group': 'Група',
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'present']
        labels = {
            'student': 'Студент',
            'subject': 'Предмет',
            'date': 'Дата',
            'present': 'Присутній',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['subject', 'name', 'description', 'deadline']
        labels = {
            'subject': 'Предмет',
            'name': 'Назва завдання',
            'description': 'Опис завдання',
            'deadline': 'Крайній термін',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'assignment', 'grade']
