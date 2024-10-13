from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)
    pin = forms.CharField(widget=forms.PasswordInput, max_length=4)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'pin', 'password1', 'password2']

class UpdateProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'phone_number']
