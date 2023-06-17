from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm, \
    UserCreationForm
from django.contrib.auth.password_validation import validate_password

from management.crm_modules.mixins import FormControlMixin, FormUserMixin

from .models import User


class UserForm(FormControlMixin, UserCreationForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, validators=[validate_password, ])
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'phone', 'role', 'organization'
        )
        field_order = fields

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for _field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class LoginUserForm(FormControlMixin, AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Логин'}), required=True)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}),
                               required=True)


class PasswordUpdateForm(FormControlMixin, FormUserMixin, PasswordChangeForm):
    pass


class PasswordReseForm(FormControlMixin, FormUserMixin, SetPasswordForm):
    pass


class PasswordEmailForm(FormControlMixin, FormUserMixin, PasswordResetForm):
    pass
