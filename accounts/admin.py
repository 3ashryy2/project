from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserRegistrationForm, UpdateProfileForm
from .models import User

class UserAdmin(UserAdmin):
    add_form = UserRegistrationForm
    form = UpdateProfileForm
    model = User
    list_display = ['email', 'username',]

admin.site.register(User, UserAdmin)