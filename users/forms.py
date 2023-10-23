from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput, PasswordInput
from users.models import MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser
        fields = ("email",)
        widgets = {
            'email': EmailInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Пароль'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'})

