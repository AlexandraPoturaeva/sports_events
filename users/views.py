from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import MyUserCreationForm
from users.models import MyUser


class SignUpView(CreateView):
    model = MyUser
    form_class = MyUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
