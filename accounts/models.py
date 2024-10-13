# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    pin = models.CharField(max_length=255)  # User PIN for secure transactions

    def set_pin(self, raw_pin):
        """Set the hashed PIN."""
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        """Check if the raw PIN matches the stored hashed PIN."""
        return check_password(raw_pin, self.pin)

    @classmethod
    def register_user(cls, data):
        """Register a new user."""
        user = cls(
            username=data['username'],
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        user.set_password(data['password'])
        user.set_pin(data['pin'])
        user.save()
        return user

    @classmethod
    def login_user(cls, request, username, password):
        """Authenticate and log in a user."""
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return user
        return None

    @classmethod
    def logout_user(cls, request):
        """Log out the current user."""
        auth_logout(request)
