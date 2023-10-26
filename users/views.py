from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from users.models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    social_auth_redirect_url = '/'
    template_name = 'registration/signup.html'
