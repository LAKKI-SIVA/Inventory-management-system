from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import UserUIRegistrationForm

User = get_user_model()

class UserUIRegistrationView(CreateView):
    """
    HTML UI endpoint for registering a new user.
    """
    model = User
    form_class = UserUIRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('ui_login')
