from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        labels = {
            "title": "Title",
            "description": "Description",
            "is_completed": "Is Completed",
            "priority": "Priority",
        }
        fields = ['title', 'description', 'is_completed', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(
        label='Password',
        error_messages={
            'required': 'Please enter your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Password'
        }),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        error_messages={
            'required': 'Please confirm your password.'},
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Confirm Password'
        }),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'email': 'Email'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control my-class',
                'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control my-class',
                'placeholder': 'Email'
            })}
        error_messages = {
            'username': {
                'required': 'Please enter your username.',
                'invalid': 'Please enter a valid username! Use "-" or "_" instead of spaces',
            },
            'email': {
                'required': 'Please enter your email.',
            },
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(
        error_messages={
            'required': 'Please enter your username.',
            'invalid': 'Please enter a valid username! ',
        },
        widget=forms.TextInput(attrs={
            'class': 'form-control my-class',
            'placeholder': 'Full Name'
        }),

    )
    password = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={
                                   'class': 'form-control my-class',
                                   'placeholder': 'Password'
                                   }),
        error_messages={
            'required': 'Please enter your password.',
            'invalid': 'Please enter a valid password.',
        }
    )
