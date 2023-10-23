from django.contrib.auth.views import LoginView
from django.urls import path
from users.views import SignUpView
from users.forms import UserLoginForm

urlpatterns = [
    path('sign_up/', SignUpView.as_view()),
    path('login/', LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UserLoginForm
            )),
]
