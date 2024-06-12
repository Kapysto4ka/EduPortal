from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class TeacherRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super(TeacherRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = StudentAssignment
        fields = ['file', 'comment']



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email',)


class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['avatar']

class TeacherAvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['avatar']