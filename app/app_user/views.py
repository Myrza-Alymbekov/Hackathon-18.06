from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView

from .forms import LoginUserForm, PasswordEmailForm, PasswordReseForm, PasswordUpdateForm, UserForm
from .models import User


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')
    sidebar_group = 'Пользователи'
    sidebar_name = 'Создать пользователя'
    sidebar_icon = 'fas fa-user-plus'
    success_message = 'Вы успешно зарегистрировались'


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'


class PasswordUpdateView(SuccessMessageMixin, PasswordChangeView):
    model = User
    form_class = PasswordUpdateForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('login')
    success_message = 'Вы успешно поменяли свой пароль'

    def get_success_message(self, cleaned_data):
        return self.success_message


# Сброс пароля
class PasswordResetAccView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = PasswordReseForm
    template_name = 'user/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    success_message = 'Вы изменили свой пароль'

    def get_success_message(self, cleaned_data):
        return self.success_message


class PasswordEmailView(SuccessMessageMixin, PasswordResetView):
    form_class = PasswordEmailForm
    template_name = 'user/password_reset.html'
    success_url = reverse_lazy('login')
    success_message = 'Инструкция по смене пароля выслана на Вашу почту. Пожалуйста проверьте почту.' \
                      'Если ссылка со сбросом пароля не приходит на Вашу почту убедитесь, ' \
                      'что Вы правильно указали почту.'

    def get_success_message(self, cleaned_data):
        return self.success_message
