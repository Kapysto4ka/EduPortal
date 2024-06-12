from django.contrib import admin
from .models import  Group, Subject, Assignment, Student, Grade, Attendance, Teacher, StudentAssignment, CustomUser

# Register your models here.
admin.site.register(Group)
admin.site.register(Subject)
admin.site.register(Assignment)
admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Attendance)
admin.site.register(Teacher)
admin.site.register(StudentAssignment)
admin.site.register(CustomUser)