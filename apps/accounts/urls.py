from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import UserRegistrationView, UserProfileView, UserUIRegistrationView

urlpatterns = [
    # ------------------
    # HTML UI ROUTES
    # ------------------
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='ui_login'),
    path('register/', UserUIRegistrationView.as_view(), name='ui_register'),
    path('logout/', auth_views.LogoutView.as_view(), name='ui_logout'),

    # ------------------
    # REST API ROUTES
    # ------------------
    path('api/register/', UserRegistrationView.as_view(), name='api_register'),
    path('api/me/', UserProfileView.as_view(), name='api_profile'),
    path('api/login/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
