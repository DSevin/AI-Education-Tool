from django import forms
from .models import Topic, StudentResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = StudentResponse
        fields = ['student_answer']