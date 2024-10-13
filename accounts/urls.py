from django.urls import path
from .views import LoginView, LogoutView, HomeView, RegisterView, ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('home/', HomeView.as_view(), name='api_home'),
    path('register/', RegisterView.as_view(), name='api_register'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
]
