from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.views import SignUpView
from users.forms import UserLoginForm

urlpatterns = [
    path('sign_up/', SignUpView.as_view()),
    path('login/', LoginView.as_view(
            authentication_form=UserLoginForm
            )),
    path('logout/', LogoutView.as_view()),
]
