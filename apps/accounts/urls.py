from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserUIRegistrationView
urlpatterns = [
    # ------------------
    # HTML UI ROUTES
    # ------------------
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='ui_login'),
    path('register/', UserUIRegistrationView.as_view(), name='ui_register'),
    path('logout/', auth_views.LogoutView.as_view(), name='ui_logout'),
]
