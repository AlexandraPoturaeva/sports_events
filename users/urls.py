from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from users.views import SignUpView
from users.forms import UserLoginForm

urlpatterns = [
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path(
        'login/',
        LoginView.as_view(authentication_form=UserLoginForm),
        name='login',
    ),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include('social_django.urls', namespace='social')),
]
