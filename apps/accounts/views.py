from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for registering a new user.
    Uses AllowAny because a user shouldn't need a token to sign up!
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving the logged-in user's profile.
    Uses IsAuthenticated (default from settings) so only logged-in users can access it.
    """
    serializer_class = UserProfileSerializer

    def get_object(self):
        # Instead of looking up a user by ID in the URL,
        # we simply return the user attached to the current request token!
        return self.request.user

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import UserUIRegistrationForm

class UserUIRegistrationView(CreateView):
    """
    HTML UI endpoint for registering a new user.
    """
    model = User
    form_class = UserUIRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('ui_login')
