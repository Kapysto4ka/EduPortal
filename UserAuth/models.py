from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def student_count(self):
        return self.students.count()

class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='subjects')
    color = models.CharField(max_length=7, default='#FFFFFF')  

    def __str__(self):
        return self.name
    
class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    email = models.EmailField(default='')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    subjects = models.ManyToManyField(Subject, related_name='teachers')
    groups = models.ManyToManyField(Group, related_name='teachers', default='')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user.username})"

class Assignment(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assignments', default="")
    name = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    file = models.FileField(upload_to='assignments/', null=True, blank=True)

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='students', default=None)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user})"



class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='grades')
    grade = models.IntegerField()

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"

class StudentAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    completed = models.BooleanField(default=True)
    graded = models.BooleanField(default=False) 
    submission_date = models.DateTimeField(null=True, blank=True)
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.student.user.username} - {self.assignment.name}'

